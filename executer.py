from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user='root',
        password='ardbms',  # getpass("Enter password: ")
        database='sap'
    ) as connection:
        print(connection)
        create_db_query = "ALTER TABLE students ADD class VARCHAR(255)" # UPDATE `sap`.`students` SET `class` = '1052' WHERE (`id` = '1');
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
except Error as e:
    print(e)
