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

data = ("Mehdi", "Ebrahimi", "mhdi", "ebram")

# query
cursor.execute("""
    INSERT INTO teachers (name, family, username, password)
    VALUES (%s, %s, %s, %s)
""", data)

# ثبت تغییرات
db.commit()

print("data added to table ")
# closing connection
cursor.close()
db.close()
