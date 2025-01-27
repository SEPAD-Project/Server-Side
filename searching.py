import mysql.connector

def search_value(value):
    # connetcting to db
    db = mysql.connector.connect(
        host="localhost",  
        user="root",       
        password="ardbms",  
        database="sap"   
    )

    cursor = db.cursor()



    cursor.execute('SELECT password FROM students WHERE username = %s', (value,))

    result = cursor.fetchone()

    if result:
        print(f'result is {result[0]}')
    else:
        print(f'wrong value{search_value}')

    # بستن اتصال
    cursor.close()
    db.close()


search_value(input('value : '))