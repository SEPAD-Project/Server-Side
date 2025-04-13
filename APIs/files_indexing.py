from flask import Flask, request, jsonify, make_response
import os 
import configparser
import time 
from datetime import datetime
from pathlib import Path

config_path = os.path.join('../config.ini')
config = configparser.ConfigParser()
config.read(config_path)

base_path = config['Server']['schools_path']
port = int(config['Server']['file_indexing_port'])
request_log_path = Path("../"+str(config['ControlServer']['api1_log']))


def log_message(message):
    BASE_PATH = "C://sap-project//log.txt"
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(BASE_PATH, 'a') as file:
        file.write(f"[{formatted_time}] {message}\n")

def log_request(response):
    timestamp = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
    client_ip = request.remote_addr
    method = request.method
    path = request.path
    protocol = request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1')
    status_code = response.status_code
    log_line = f'[{timestamp}] - {client_ip} - "{method} {path} {protocol}" {status_code} -\n'
    with open(request_log_path, 'a') as log_file:
        log_file.write(log_line)
        log_file.close()
    
    return response

app = Flask(__name__)

@app.before_request
def log_before_request():
    pass

@app.after_request
def log_after_request(response):
    log_request(response)
    return response

@app.errorhandler(404)
def handle_404(e):
    response = make_response(jsonify({"error": "Not found"}), 404)
    return response

@app.errorhandler(500)
def handle_500(e):
    response = make_response(jsonify({"error": "Internal server error"}), 500)
    return response

# API for getting students list
@app.route('/get_students', methods=['POST'])
def get_students():
    data = request.get_json()
    school_name = data.get("school_name")
    class_code = data.get("class_code")

    class_path = os.path.join(base_path, school_name, class_code)
    student_list_file = os.path.join(class_path, f"students{class_code}{school_name}.txt")

    if not os.path.exists(student_list_file):
        log_message('FILES INDEXING | Class or school not found')
        return jsonify({"error": "Class or school not found"}), 404

    with open(student_list_file, 'r', encoding='utf-8') as file:
        students = [line.strip() for line in file.readlines()]

    return jsonify({"students": students})

# API for getting last message
@app.route('/get_last_message', methods=['POST'])
def get_last_message():
    data = request.get_json()
    school_name = data.get("school_name")
    class_code = data.get("class_code")
    student_name = data.get("student_name")

    class_path = os.path.join(base_path, school_name, class_code)
    student_file = os.path.join(base_path, school_name, class_code, f"{student_name}.txt")

    if not os.path.exists(class_path):
        log_message('FILES INDEXING | class not found')
        return jsonify({"error": "class not found"}), 404

    if not os.path.exists(student_file):
        log_message('FILES INDEXING | Student not found')
        return jsonify({"error": "Student not found"}), 404

    with open(student_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    last_message = lines[-1].strip() if lines else "No messages yet"
    
    return jsonify({"student": student_name, "message": last_message})

if __name__ == '__main__':
    debug_stat = False
    with open(request_log_path, 'a') as log_file:
        log_file.write(f'* Serving Flask app "{str(__file__).split('\\')[-1]}"\n* Debug mode: {debug_stat}\n* Running on all addresses (0.0.0.0)\n* Running on http://127.0.0.1:{port}')
        log_file.close()
    app.run(host="0.0.0.0", port=port, debug=debug_stat)