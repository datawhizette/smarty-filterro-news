import os
from functools import wraps

from flask import Flask, render_template, request
from flask_cors import CORS
import pandas as pd

import mail as m
from models import add_user, scrape, wrap_output_in_html

import smtplib

from nltk.sentiment import SentimentIntensityAnalyzer

EMAIL_ADDRESS = "smartyfilterro@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)

CORS(app)

def with_app_context(func):
    @wraps(func)
    def _func(*args, **kwargs):
        with app.app_context():
            return func(*args, **kwargs)
    return _func
    
@with_app_context
def send_newsletter_email(name, emails, mail_template, source, topics, time_bed):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    if type(emails)==list:
        emaillist = [elem.strip().split(',') for elem in emails]
    else: emaillist = [emails]
    message_template = m.read_template(mail_template)

    msg = MIMEMultipart()
    message = message_template.substitute(PERSON_NAME=name.title())

    msg['Subject'] = 'FIRST NEWSLETTER'
    msg['From'] = EMAIL_ADDRESS

    msg.attach(MIMEText(message, 'plain'))

    all_news = pd.DataFrame()
    if 'technology' in topics:
        output=scrape('https://www.reuters.com/news/archive/innovationNewsTechMediaTelco',source)
        all_news=all_news.append(output)
    if 'markets' in topics:
        output=scrape('https://www.reuters.com/news/archive/marketsNews',source)
        all_news=all_news.append(output)
    
    all_news = all_news.drop_duplicates(subset=['title'])
    if time_bed == "Yes":
        sia = SentimentIntensityAnalyzer()
        all_news['positivity'] = all_news['title'].apply(lambda x: sia.polarity_scores(x)['pos'])
        all_news['negativity'] = all_news['title'].apply(lambda x: sia.polarity_scores(x)['neg'])
        all_news = all_news[(all_news.positivity>=0.1)&(all_news.negativity<=0.1)].iloc[:,:-2]
    html = wrap_output_in_html(all_news.dropna().reset_index(drop=True))
    newspart = MIMEText(html,_subtype='html')
    msg.attach(newspart)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(msg['From'], emaillist, msg.as_string())
        
    del msg


@app.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        sources = ['BBC', 'CNN', 'Bloomberg', 'All Sources', 'Reuters']
        topics = ['Technology', 'Entertainment', 'Politics', 'All Topics']
        time_bed_options = ['Yes', 'No']
        news_times = ['Daily in the morning', 'Daily in the evening', 'Weekly']

    if request.method == 'POST':
        source = request.form.get('sources')
        name = request.form.get('name')
        email = request.form.get('email')
        time_bed = request.form.get('time-bed-mode')
        news_time = request.form.get('news_times')
        topics = request.form.getlist('get-topics')
        try:
            add_user(name, email, source, topics, time_bed, news_time)
            m.send_confirmation_email(EMAIL_ADDRESS, EMAIL_PASSWORD, name, email, "message.txt")
            
            send_newsletter_email(name, email, "first_newsletter.txt", source, topics, time_bed)
            return render_template('success.html')
        except Exception as e:
            print (e)
            return render_template('failure.html')



    return render_template('index.html', sources=sources, topics=topics, time_bed_options=time_bed_options, news_times=news_times)

if __name__ == '__main__':
    app.run(debug=True)