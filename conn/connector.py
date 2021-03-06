import psycopg2, pymysql
import traceback
import sys



class DBConnector():
    def __init__(self, db_name, db_user, db_password, db_host, db_port, db_type):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_type = db_type
        self.create_connection()

    def create_connection(self):
        self.create_connection=None
        try:
            if self.db_type == "postgres":
                self.connection = psycopg2.connect(
                    database=self.db_name,
                    user=self.db_user,
                    password=self.db_password,
                    host=self.db_host,
                    port=self.db_port,
                )
            if self.db_type == "mysql":
                self.connection = pymysql.connect(
                    database=self.db_name,
                    user=self.db_user,
                    password=self.db_password,
                    host=self.db_host,
                    port=self.db_port,
                )
            print("Connection to PostgreSQL DB successful")
        except Exception as e:
            print(f"The error '{e}' occurred")
        return self.connection

    def read_query(self,query):
        try:
            cursor = self.connection.cursor()
        except:
            print('Check connection to db')
            return
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"The error '{e}' occurred")
