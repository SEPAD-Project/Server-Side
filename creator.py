import mysql.connector


db = mysql.connector.connect(
    host="localhost",  
    user="root",    
    password="ardbms" 
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS school")
print('Database Created')

# connect to database school
db.database = "sap"

# creating table students
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        family VARCHAR(255),
        national_code VARCHAR(255),
        username VARCHAR(255),
        password VARCHAR(255),
        class VARCHAR(255),
        uid VARCHAR(255),
        school VARCHAR(255),
    )
""")

# closing connection
cursor.close()
db.close()

print("Table [students] Created")



