import psycopg2,re

DATABASE_URL = 'postgres://seaotter:Ersl2kH5sG2IOiEzrFQLsh4kI5NDcyTi@dpg-ce7jktarrk049r63khs0-a.oregon-postgres.render.com/seaotterhimedb'


conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("SELECT * from userDetails")
rows = cursor.fetchall()
db1 = []
db2 = []
db3 = []
db4 = []
db5 = []
for row in rows:
    db1.append(row[0])
    db2.append(row[1])
    db3.append(row[2])
    db4.append(row[3])
for i in range(len(db1)):
    db5.append(f"{str(db1[i])}|{str(db2[i])}|{str(db3[i])}|{str(db4[i])}")
db5 = str(db5)
db5 = re.sub("\[|\'|\]","",db5)
print(db5.replace(', ',"\n"))