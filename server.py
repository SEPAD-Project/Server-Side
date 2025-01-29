from flask import Flask, request, jsonify
import os
import mysql.connector
from mysql.connector import Error
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

# conecting to db
db_config = {
    'host': 'localhost',
    'database': 'sap',
    'user': 'root',
    'password': 'ardbms'
}

base_path = r'C:\sap-project\server'
# getting user passwords from db
def getting_pass_from_db(username):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM students WHERE username = %s ", (username,))
        password_in_db = cursor.fetchone()[0]
        connection.close()
        return password_in_db
    except Error as e:
        print(f"error while connectoin to db {e}")
        return None

# get and save data
@app.route('/upload_text', methods=['POST'])
def upload_text():
    # getting data from post requests
    username = request.form['username']
    password = request.form['password']
    school_name = request.form['school_name']
    class_code = request.form['class_code']
    text = request.form['text']
    print(username)
    print(password)


    if getting_pass_from_db(username) != password:
        return jsonify({"Error": "incorrect data"}), 401
    
    elif getting_pass_from_db(username) == password:
        # make folder and save text to file
        school_path = os.path.join(base_path, school_name)
        class_path = os.path.join(school_path, class_code)

        # make folder if they dont exist
        os.makedirs(class_path, exist_ok=True)

        file_path = os.path.join(class_path, f"{username}.txt")

        # saving text to file
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(text + '\n')

        return jsonify({"message": "text successfully saved"}), 200

if __name__ == '__main__':
    # running wsgiserver
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
