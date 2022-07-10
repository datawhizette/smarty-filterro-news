import smtplib
import os
from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def send_confirmation_email(input_email, input_password, name, email, mail_template):
    message_template = read_template(mail_template)

    msg = MIMEMultipart()
    message = message_template.substitute(PERSON_NAME=name.title())

    msg['Subject'] = 'NEWSLETTER SUBSCRIPTION'
    msg['From'] = input_email
    msg['To'] = email

    msg.attach(MIMEText(message, 'plain'))

    with open('img/penguin_greeting.jpg', 'rb') as f:
        file_data = f.read()
        file_name = f.name

    img = MIMEImage(file_data, _subtype="jpg")
    img.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name)
    msg.attach(img)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(input_email, input_password)
        smtp.send_message(msg)
        
    del msg