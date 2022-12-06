import psycopg2,re

DATABASE_URL = 'postgres://seaotter:Ersl2kH5sG2IOiEzrFQLsh4kI5NDcyTi@dpg-ce7jktarrk049r63khs0-a.oregon-postgres.render.com/seaotterhimedb'


conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("SELECT Input, Output from Words")
rows = cursor.fetchall()
db1 = []
db2 = []
db3 = []
for row in rows:
    db1.append(row[0])
    db2.append(row[1])
for i in range(len(db1)):
    db3.append(f"{str(db1[i])} ---> {str(db2[i])}")
db3 = str(db3)
db3 = re.sub("\[|\'|\]","",db3)
print(db3.replace(', ',"\n"))