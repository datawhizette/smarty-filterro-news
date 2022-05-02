import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mail import read_template
from models import scrape, wrap_output_in_html
from app import EMAIL_ADDRESS, EMAIL_PASSWORD

EMAIL_ADDRESS = "smartyfilterro@gmail.com"
# os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = "102938qw"
# os.environ.get('EMAIL_PASSWORD')

def send_newsletter_email(name, emails, mail_template, source, topic, time_bed):
    if type(emails)==list:
        emaillist = [elem.strip().split(',') for elem in emails]
    else: emaillist = [emails]
    message_template = read_template(mail_template)

    msg = MIMEMultipart()
    message = message_template.substitute(PERSON_NAME=name.title())

    msg['Subject'] = 'FIRST NEWSLETTER'
    msg['From'] = EMAIL_ADDRESS

    msg.attach(MIMEText(message, 'plain'))

    output=scrape('https://www.reuters.com/news/archive/europe',source)
    html = wrap_output_in_html(output)
    newspart = MIMEText(html,_subtype='html')
    msg.attach(newspart)


    # conn = sqlite3.connect('news_store.db')
    # cursor = conn.execute(f'SELECT * FROM user_database WHERE email={email}')
    # result = cursor.fetchone()
    # name, source, topic

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(msg['From'], emaillist, msg.as_string())
        
    del msg
