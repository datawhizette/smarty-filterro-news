import sqlite3
import pandas as pd

conn = sqlite3.connect('news_store.db')
cursor = conn.execute(''' SELECT * FROM news ''')
result = cursor.fetchall()

print (f"Size of the DB: {len(result)}")
print (result[0])