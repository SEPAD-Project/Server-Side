import mysql.connector

# connect to DB
db = mysql.connector.connect(
    host="localhost",  
    user="root",       
    password="ardbms",  
    database="sap"   
)

cursor = db.cursor()

# Data
data = ("Abolfazl", "Rashidian", "09233333", "1", "1", 1052)

# query
cursor.execute("""
    INSERT INTO students (name, family, national_code, username, password, class)
    VALUES (%s, %s, %s, %s, %s, %s)
""", data)

# ثبت تغییرات
db.commit()

print("data added to table ")
# closing connection
cursor.close()
db.close()
