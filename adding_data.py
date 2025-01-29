import mysql.connector

# connect to DB
db = mysql.connector.connect(
    # host="localhost",  
    # user="root",       
    # password="ardbms",  
    # database="sap"   
    host="185.4.28.110",  
    user="root", # sapacc - ardbms
    port=5000,   
    password="sapprogram2583",
    database='sap'
)

cursor = db.cursor()

# Data
data = ("Abolfazl", "Rashidian", "09233333", "test", "pass", 1052, 1111111111, 'hnsch1')

# query
cursor.execute("""
    INSERT INTO students (name, family, national_code, username, password, class, uid, school)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", data)

# ثبت تغییرات
db.commit()

print("data added to table ")
# closing connection
cursor.close()
db.close()
