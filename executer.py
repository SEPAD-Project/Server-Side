from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user='root',
        password='ardbms',  # getpass("Enter password: ")
    ) as connection:
        print(connection)
        create_db_query = "CREATE DATABASE sap"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
except Error as e:
    print(e)
