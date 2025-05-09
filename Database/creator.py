import mysql.connector

db = mysql.connector.connect(
    host="185.4.28.110",  
    user="root",
    port=5000,   
    password="sapprogram2583" 
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS sap")
print('"SAP" DATABASE CREATED.')

# connect to database school
db.database = "sap"

# Creating students table
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS students (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         student_name VARCHAR(255),
#         student_family VARCHAR(255),
#         student_national_code VARCHAR(255),
#         student_password VARCHAR(255),
#         class_code VARCHAR(255),
#         school_code VARCHAR(255)
#     )
# """)
# print('"STUDENTS" TABLE CREATED.')

# Creating teachers table
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS teachers (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         teacher_name VARCHAR(255),
#         teacher_family VARCHAR(255),
#         teacher_national_code VARCHAR(255),
#         teacher_password VARCHAR(255),
#         teacher_classes VARCHAR(255),
#         lesson VARCHAR(255)
#     )
# """)
# print('"TEACHERS" TABLE CREATED.')

# Creating classes table
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS classes (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         class_name VARCHAR(255),
#         class_code VARCHAR(255),
#         school_code VARCHAR(255),
#         teachers VARCHAR(255)
#     )
# """)
# print('"CLASSES" TABLE CREATED.')

# Creating schools table
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS schools (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         school_name VARCHAR(255),
#         school_code VARCHAR(255),
#         manager_personal_code VARCHAR(255),
#         province VARCHAR(255),
#         city VARCHAR(255),
#         teachers VARCHAR(255),
#         email VARCHAR(255)               
#     )
# """)
# print('"SCHOOLS" TABLE CREATED.')

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS admins (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         username VARCHAR(255),
#         password VARCHAR(255)
#     )
# """)
# print('"admins" TABLE CREATED.')

# closing connection
cursor.close()
db.close()
