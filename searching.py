import mysql.connector

def search_value(value, person, host='localhost', user='root', password='ardbms', database='sap'):
    # connetcting to db
    db = mysql.connector.connect(
        # host=host,  
        # user=user,       
        # password=password,  
        # database=database 
    host="185.4.28.110",  
    user="root", # sapacc - ardbms
    port=5000,   
    password="sapprogram2583",
    database=database
    )
    cursor = db.cursor()
    if person == 'student' :
        cursor.execute("SELECT COUNT(*) FROM students WHERE username = %s", (value,))
        result = cursor.fetchone()
        if result[0] > 0:
            cursor.execute('SELECT name, family, password, username, class, school, uid, national_code class FROM students WHERE username = %s', (value,))

            result = cursor.fetchone()
            cursor.close()
            db.close()

            if result:
                return(result)
            else:
                return(False)
        else:
            cursor.close()
            db.close()
            return ('not found')
        
    elif person == 'teacher' :
        cursor.execute("SELECT COUNT(*) FROM teachers WHERE username = %s", (value,))
        result = cursor.fetchone()
        if result[0] > 0: # if user exist, return his/her information including password
            cursor.execute('SELECT name, family, password FROM teachers WHERE username = %s', (value,))
            result = cursor.fetchone()
            cursor.close()
            db.close()
            if result:
                return(result)
            else:
                return(False)
        else:
            cursor.close()
            db.close()
            return ('not found') # returning not found if user not exists

if __name__ == '__main__' :
    x = input('value : ')
    print(search_value(value=x, person='student'))