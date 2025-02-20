import mysql.connector


db = mysql.connector.connect(
    host="185.4.28.110",  
    user="root", # sapacc - ardbms
    port=5000,   
    password="sapprogram2583" 
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS sap")
print('Database Created')

# connect to database school
db.database = "sap"

# creating table students
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_name VARCHAR(255),
        student_family VARCHAR(255),
        student_national_code VARCHAR(255),
        student_password VARCHAR(255),
        class_code VARCHAR(255),
        school_code VARCHAR(255)
    )
""")
print("Table [students] Created")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        teacher_name VARCHAR(255),
        teacher_family VARCHAR(255),
        teacher_national_code VARCHAR(255),
        teacher_password VARCHAR(255),
        teacher_classes VARCHAR(255)
    )
""")
print("Table [teachers] Created")


# closing connection
cursor.close()
db.close()




