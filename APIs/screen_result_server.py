import os
import json
from flask import Flask, request, jsonify, make_response
from werkzeug.exceptions import BadRequest
import configparser
import time 
from datetime import datetime
from pathlib import Path

config_path = os.path.join('../config.ini')
config = configparser.ConfigParser()
config.read(config_path)
base_path = config['Server']['schools_path']
port = int(config['Server']['screen_result_server_port'])
request_log_path = Path("../"+str(config['ControlServer']['api3_log']))

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

def validate_parameters(data):
    """Validate required parameters in request"""
    required = ['school', 'class', 'student_id', 'windows']
    if not all(key in data for key in required):
        log_message("SCREEN RESULT SERVER | Missing required parameters")
        raise BadRequest('Missing required parameters')

def get_student_path(school, class_name, student_id):
    """Generate file path based on parameters"""
    base_dir = os.path.join(
        base_path,
        school.replace(' ', '_'),
        class_name.replace(' ', '_')
    )
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, f'{student_id}.json')

@app.route('/save', methods=['POST'])
def save_data():
    """API endpoint to save window data"""
    try:
        data = request.get_json()
        validate_parameters(data)
        
        file_path = get_student_path(
            data['school'],
            data['class'],
            data['student_id']
        )
        
        with open(file_path, 'w') as f:
            json.dump(data['windows'], f)
            
        return jsonify({'status': 'success'}), 200
    
    except BadRequest as e:
        log_message(f"SCREEN RESULT SERVER | {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log_message(f"SCREEN RESULT SERVER | {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/get', methods=['GET'])
def get_data():
    """API endpoint to retrieve window data"""
    try:
        school = request.args.get('school')
        class_name = request.args.get('class')
        student_id = request.args.get('student_id')
        
        if not all([school, class_name, student_id]):
            log_message(f"SCREEN RESULT SERVER | Missing parameters")
            raise BadRequest('Missing parameters')
            
        file_path = get_student_path(school, class_name, student_id)
        
        if not os.path.exists(file_path):
            log_message(f"SCREEN RESULT SERVER | Data not found")
            return jsonify({'error': 'Data not found'}), 404
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        return jsonify(data), 200
    
    except BadRequest as e:
        log_message(f"SCREEN RESULT SERVER | {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log_message(f"SCREEN RESULT SERVER | {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    log_message(f"SCREEN RESULT SERVER | Server started on port {port} ")

    app.run(host='0.0.0.0', port=port, threaded=True)