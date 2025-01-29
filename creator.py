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
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS students (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         name VARCHAR(255),
#         family VARCHAR(255),
#         national_code VARCHAR(255),
#         username VARCHAR(255),
#         password VARCHAR(255),
#         class VARCHAR(255),
#         uid VARCHAR(255),
#         school VARCHAR(255)
#     )
# """)
# print("Table [students] Created")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        family VARCHAR(255),
        username VARCHAR(255),
        password VARCHAR(255)
    )
""")

# closing connection
cursor.close()
db.close()

print("Table [teachers] Created")



