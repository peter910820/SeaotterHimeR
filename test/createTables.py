import os
import psycopg2

DATABASE_URL = 'postgres://seaotter:Ersl2kH5sG2IOiEzrFQLsh4kI5NDcyTi@dpg-ce7jktarrk049r63khs0-a.oregon-postgres.render.com/seaotterhimedb'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE Words(
    ID serial PRIMARY KEY,
    Input VARCHAR (50) NOT NULL,
    Output VARCHAR (50) NOT NULL,
    Time VARCHAR (50) NOT NULL,
    Date VARCHAR (50) NOT NULL);''')
conn.commit()

cursor.close()
conn.close()