import mysql.connector
import json
# connect to DB
db = mysql.connector.connect(
    host="185.4.28.110",  
    user="root", # sapacc - ardbms
    port=5000,   
    password="sapprogram2583",
    database='sap'
)

cursor = db.cursor()

classes_list = ['7b#2f31627', '7b#2f31626', '7b#2f31625']
classes = json.dumps(classes_list)
data = ("mehrdad", 'najafi', 'mhrd', 'pass', str(classes))

# # query
# cursor.execute("""
#     INSERT INTO teachers (teacher_name, teacher_family, teacher_national_code, teacher_password, teacher_classes)
#     VALUES (%s, %s, %s, %s, %s)
# """, data)

# db.commit()

data = ('Abolfazl', 'Rashidian', '0929577777', 'stpass', '1052xx', 'hn1xxx')
cursor.execute("""
    INSERT INTO students (student_name, student_family, student_national_code, student_password, class_code, school_code)
    VALUES (%s, %s, %s, %s, %s, %s)
""", data)

db.commit()

print("data added to table ")
# closing connection
cursor.close()
db.close()
