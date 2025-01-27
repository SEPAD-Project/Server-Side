import mysql.connector

def search_value(value, host='localhost', user='root', password='ardbms', database='sap', 
                search_by='username', data='password'):
    # connetcting to db
    db = mysql.connector.connect(
        host=host,  
        user=user,       
        password=password,  
        database=database  
    )
    cursor = db.cursor()
    cursor.execute('SELECT password FROM students WHERE username = %s', (value,))

    result = cursor.fetchone()
    # closing connectoin
    cursor.close()
    db.close()

    if result:
        # print(f'result in searching.py search_value func is --->>> {result[0]}')
        return(f'{result[0]}')
    else:
        return(False)



if __name__ == '__main__' :
    x = input('value : ')
    search_value(value=x)