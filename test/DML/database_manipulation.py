import os
import psycopg2
import re

from dotenv import load_dotenv


class DatabaseManipulation(object):
    def __init__(self) -> None:
        load_dotenv()
        self.database_url = os.getenv("DATABASE_URL")

    def insert_data_for_words(self) -> None:
        conn = psycopg2.connect(self.database_url, sslmode='require')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Words (Input, Output, Time, Date) VALUES (%s,%s,%s,%s)",
                       ("test", "chicken", '0922', '0923'))
        conn.commit()

        cursor.close()
        conn.close()

    # delete account
    def delete_data_for_userdetails(self) -> None:
        conn = psycopg2.connect(self.database_url, sslmode='require')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, username, password, createtime from userDetails")
        rows = cursor.fetchall()
        x = input("Input delete account name: ")
        for i in range(len(rows)):
            if x == rows[i][1]:
                cursor.execute(
                    "DELETE from userDetails where username=(%s)", (x,))
                conn.commit()
                print("Delete success!")

        cursor.close()
        conn.close()

    def query_data_for_words(self) -> None:
        conn = psycopg2.connect(self.database_url, sslmode='require')
        cursor = conn.cursor()

        cursor.execute("SELECT Input, Output from Words")
        rows = cursor.fetchall()
        db1, db2, db3 = [], [], []
        for row in rows:
            db1.append(row[0])
            db2.append(row[1])
        for i in range(len(db1)):
            db3.append(f"{str(db1[i])} ---> {str(db2[i])}")
        db3 = str(db3)
        db3 = re.sub("\\[|\'|\\]", "", db3)
        print(db3.replace(', ', "\n"))

    def query_data_for_userdetails(self) -> None:
        conn = psycopg2.connect(self.database_url, sslmode='require')
        cursor = conn.cursor()

        cursor.execute("SELECT * from userDetails")
        rows = cursor.fetchall()
        db1, db2, db3, db4, db5 = [], [], [], [], []
        for row in rows:
            db1.append(row[0])
            db2.append(row[1])
            db3.append(row[2])
            db4.append(row[3])
        for i in range(len(db1)):
            db5.append(
                f"{str(db1[i])}|{str(db2[i])}|{str(db3[i])}|{str(db4[i])}")
        db5 = str(db5)
        db5 = re.sub("\\[|\'|\\]", "", db5)
        print(db5.replace(', ', "\n"))
