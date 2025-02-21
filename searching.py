import mysql.connector

def get_values_by_username(value, person, host='localhost', user='root', password='ardbms', database='sap'):
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
    value = str(value)
    cursor = db.cursor()
    if person == 'student' :
        cursor.execute("SELECT COUNT(*) FROM students WHERE student_national_code = '{}'".format(value))
        result = cursor.fetchone()
        print(result)
        if result[0] > 0:
            cursor.execute('SELECT student_name, student_family, student_password, class_code, school_code, student_national_code class FROM students WHERE student_national_code = %s', (value,))

            udata = cursor.fetchone()
            cursor.close()
            db.close()

            if udata:
                return(udata)
            else:
                return(False)
        else:
            cursor.close()
            db.close()
            return ('not found')
        
    elif person == 'teacher' :
        cursor.execute("SELECT COUNT(*) FROM teachers WHERE teacher_national_code = %s", (value,))
        result = cursor.fetchone()
        if result[0] > 0: # if user exist, return his/her information including password
            cursor.execute('SELECT teacher_name, teacher_family, teacher_password, teacher_classes FROM teachers WHERE teacher_national_code = %s', (value,))
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
    print(get_values_by_username(value=x, person='student'))