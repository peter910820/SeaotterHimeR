import os
import psycopg2

DATABASE_URL = 'postgres://seaotter:Ersl2kH5sG2IOiEzrFQLsh4kI5NDcyTi@dpg-ce7jktarrk049r63khs0-a.oregon-postgres.render.com/seaotterhimedb'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("SELECT id, username, password, createtime from userDetails")
rows = cursor.fetchall()
x = input("Input delete account name: ")
for i in range(len(rows)):
    if x == rows[i][1]:
        cursor.execute("DELETE from userDetails where username=(%s)",(x,))
        conn.commit()
        print("Delete success!")

cursor.close()
conn.close()