import os
import psycopg2

from dotenv import load_dotenv


class CreateTable(object):
    def __init__(self) -> None:
        load_dotenv()
        self.database_url = os.getenv("DATABASE_URL")

    def create_account_table(self) -> None:
        conn = psycopg2.connect(self.database_url, sslmode='require')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE userDetails(
            id serial PRIMARY KEY,
            username VARCHAR (50) NOT NULL,
            password VARCHAR (50) NOT NULL,
            createtime VARCHAR (50) NOT NULL);''')
        conn.commit()

        cursor.close()
        conn.close()

    def create_words_table(self) -> None:
        conn = psycopg2.connect(self.database_url, sslmode='require')
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
