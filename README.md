## Smart Newsletter
A quick project on filtering news to get well informed and not overwhelmed. Filtered newsletters are sent straight to your inbox. The project was done as part of WAI Practice program (educational program for Women in AI).

Technologies used:
- **Python** Data mining - requests; BeautifulSoup; sending emails with the smtplib library.
- **Flask** Web Application Interface.
- **SQL** Storing news and new service subscribers in the database.

## Instructions 
Run
```
python app.py
```
to start the application on http://127.0.0.1:5000.

Enter your preferences on that web page such as news source, category of news, bedtime mode (filter out news that can increase stress level leading to insomnia), and time when to send a regular newsletter.

As a result, you will first get a service subscription confirmation email, then your first tailored newsletter to your inbox.


----------------------------------
## TO DO
- Automate process of sending regular newsletters to subscribed users
- Dockerise app and host it in a cloud
- Add docstrings
- Add unit tests.
