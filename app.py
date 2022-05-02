from flask import Flask, render_template, request
from flask_cors import CORS
from models import add_user
import mail as m
import newsletter_email as ne

EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""
# os.environ.get('EMAIL_PASSWORD')

app = Flask(__name__)

CORS(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        sources = ['BBC', 'CNN', 'Bloomberg', 'Reuters', 'All Sources']
        topics = ['Technology', 'Entertainment', 'Politics', 'All Topics']
        time_bed_options = ['Yes', 'No']
        news_times = ['Daily in the morning', 'Daily in the evening', 'Weekly']

    if request.method == 'POST':
        source = request.form.get('sources')
        topic = request.form.get('topics')
        name = request.form.get('name')
        email = request.form.get('email')
        time_bed = request.form.get('time_bed_options')
        news_time = request.form.get('news_times')
        try:
            add_user(name, email, source, topic, time_bed, news_time)
            m.send_confirmation_email(name, email, "message.txt")
            ne.send_newsletter_email(name, email, "first_newsletter.txt", source, topic, time_bed)
            return render_template('success.html')
        except Exception as e:
            print (e)
            return render_template('failure.html')



    return render_template('index.html', sources=sources, topics=topics, time_bed_options=time_bed_options, news_times=news_times)

if __name__ == '__main__':
    app.run(debug=True)