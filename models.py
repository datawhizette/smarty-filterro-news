import sqlite3 as sql
from os import path
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import sqlite3
import re
import time

ROOT = path.dirname(path.relpath((__file__)))

def add_user(name, email, source, topic, time_bed, news_time):
    con = sql.connect(path.join(ROOT, 'user_database.db'))
    cur = con.cursor()
    try:
        cur.execute('replace into users (email, name, source, topic, time_bed, news_time) values(?, ?, ?, ?, ?, ?)', (email, name, source, topic, time_bed, news_time))
    except:
        cur.execute(f"""CREATE TABLE users (
                    email TEXT,
                    name TEXT,
                    source TEXT,
                    topic TEXT,
                    time_bed TEXT,
                    news_time TEXT)""")
    con.commit()
    con.close()


def database(df): 
    temp=[]
    conn = sqlite3.connect('news_store.db')
    c = conn.cursor()

    c.execute(f"""CREATE TABLE IF NOT EXISTS news (
    title TEXT,
    link TEXT,
    image TEXT,
    date TEXT)""")

    for i in range(len(df)):
        try:
            c.execute("""INSERT INTO news VALUES (?,?,?,?)""",df.iloc[i,:])
            conn.commit()
            temp.append(i)
            
        except Exception as e:
            print(e)
    
    conn.close()
    
    if temp:
        output=df.loc[[i for i in temp]]
        output.reset_index(inplace=True,drop=True)
    else:
        output=pd.DataFrame()
        output['title']=['No updates yet.']
        output['link']=output['image']=['']
    
    return output

def reuters(page):
    title,link,image,date =[],[],[],[]
    df=pd.DataFrame()
    
    prefix='https://www.reuters.com'
        
    for i in page.find('div', class_='news-headline-list').find_all('h3'):
        temp=i.text.replace('								','')
        title.append(temp.replace('\n',''))
    
    for j in page.find('div', class_='news-headline-list').find_all('a'):
        link.append(prefix+j.get('href'))
    link=link[0::2]
        
    for k in page.find('div', class_='news-headline-list').find_all('img'):
        if k.get('org-src'):
            image.append(k.get('org-src'))
        else:
            image.append('')

    for k in page.find('div', class_='news-headline-list').find_all('span'):
        date.append(k.text)

    
    df['title']=title
    df['link']=link
    df['image']=image
    df['date'] = date
    
    return df

def scrape(url,method):
    
    print('scraping webpage effortlessly')
    time.sleep(5)
    
    session=requests.Session()
    response = session.get(url,headers={'User-Agent': 'Mozilla/5.0'})      
    page=bs(response.content,'html.parser',from_encoding='utf_8_sig')
    
    if method == "Reuters":
        df=reuters(page)
    else: 
        raise ValueError ("This source is not supported yet!")
    df.reset_index(inplace=True,drop=True)

    for i in range(len(df)):
        if 'https://' not in df['link'][i]:
            temp=re.search('www',df['link'][i]).start()
            df.at[i,'link']='http://'+df['link'][i][temp:]

    out=database(df)
    
    return out

def wrap_output_in_html(output):
    html="""\
    <html>
    <head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title></title>
    <!--[if (mso 16)]>
    <style type="text/css">
    a {text-decoration: none;}
    </style>
    <![endif]-->
    <!--[if gte mso 9]><style>sup 
    { font-size: 100% !important; }</style><![endif]-->
    </head>
    <body>
    <div class="es-wrapper-color">
        <!--[if gte mso 9]>
                <v:background xmlns:v="urn:schemas-microsoft-com:vml" 
                fill="t">
                    <v:fill type="tile" color="#333333"></v:fill>
                </v:background>
            <![endif]-->
        <table class="es-content-body" width="600" 
        cellspacing="15" cellpadding="15" bgcolor="#ffffff" 
        align="center">
        <tr>
            <td class="esd-block-text" align="center">
            <h2>Middle East</h2></td>
        </tr></table>
        <div><br></div>
        
    """
    
    for i in range(len(output)):
        html+="""<table class="es-content-body" width="600" 
        cellspacing="10" cellpadding="5" bgcolor="#ffffff"
        align="center">"""
        html+="""<tr><td class="esd-block-text es-p10t es-p10b"
        align="center"><p><a href="%s">
        <font color="#6F6F6F">%s<font><a></p></td></tr>
        <tr><td align="center">
        <img src="%s" width="200" height="150"/></td></tr>
        <tr>"""%(output['link'][i],output['title'][i],output['image'][i])
        html+="""</tr></table><div><br></div>"""
        
    html+="""
    </div>
    </body>
    </html>
    """

    return html