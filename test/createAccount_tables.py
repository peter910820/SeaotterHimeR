import psycopg2

DATABASE_URL = 'postgres://seaotter:Ersl2kH5sG2IOiEzrFQLsh4kI5NDcyTi@dpg-ce7jktarrk049r63khs0-a.oregon-postgres.render.com/seaotterhimedb'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE userDetails(
    id serial PRIMARY KEY,
    username VARCHAR (50) NOT NULL,
    password VARCHAR (50) NOT NULL,
    createtime VARCHAR (50) NOT NULL);''')
conn.commit()

cursor.close()
conn.close()