import psycopg2

DATABASE_URL = 'postgres://seaotter:Ersl2kH5sG2IOiEzrFQLsh4kI5NDcyTi@dpg-ce7jktarrk049r63khs0-a.oregon-postgres.render.com/seaotterhimedb'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("INSERT INTO Words (Input, Output, Time, Date) VALUES (%s,%s,%s,%s)", ("test","chicken",'0922','0923'))
conn.commit()

cursor.close()
conn.close()