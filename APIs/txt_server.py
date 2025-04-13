import os
from flask import Flask, request, jsonify, make_response
from werkzeug.exceptions import BadRequest
from pymysql import connect
from pymysql import Error
import configparser
import time 
from datetime import datetime
from pathlib import Path

# Configuration setup
config_path = os.path.join('../config.ini')
config = configparser.ConfigParser()
config.read(config_path)

# Server configuration
port = int(config['Server']['txt_server_port'])
base_path = config['Server']['schools_path']
allowed_application = "SchoolApp"
required_header = "X-Application"
request_log_path = Path("../"+str(config['ControlServer']['api4_log']))

# Database configuration
db_config = {
    'host': config['Database']['Host'],
    'database': config['Database']['Database'],
    'port': int(config['Database']['DB_port']),
    'user': config['Database']['User'],
    'password': config['Database']['Password']
}

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

def validate_application_header():
    """Validate the request contains required application header"""
    app_header = request.headers.get(required_header)
    if app_header != allowed_application:
        log_message(f"TEXT SERVER | Invalid header detected: {app_header}")
        raise BadRequest('Unauthorized application')


def authenticate_user(username, password):
    """Authenticate user against database"""
    try:
        with connect(**db_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT student_password FROM students WHERE student_national_code = %s",
                    (username,)
                )
                result = cursor.fetchone()
                if not result:
                    log_message(f"TEXT SERVER | User not found: {username}")
                    return False, 'User not found'
                if result[0] != password:
                    log_message(f"TEXT SERVER | Invalid password for user: {username}")
                    return False, 'Authentication failed'
                return True, None
    except Error as e:
        log_message(f"TEXT SERVER | Database error: {str(e)}")
        return False, f'Database error: {str(e)}'

def get_file_path(school, class_code, username):
    """Generate file path based on parameters"""
    target_path = os.path.join(
        base_path,
        school,
        class_code
    )
    
    if not os.path.exists(target_path):
        log_message(f"TEXT SERVER | Directory not found: {target_path}")
        raise FileNotFoundError('Directory does not exist')
    
    if not os.access(target_path, os.W_OK):
        log_message(f"TEXT SERVER | Directory not writable: {target_path}")
        raise PermissionError('Directory not writable')
    
    return os.path.join(target_path, f"{username}.txt")

@app.route('/upload_text', methods=['POST'])
def upload_text():
    """API endpoint to save student text"""
    try:
        validate_application_header()

            
        # Data validation
        required_fields = ['username', 'password', 'school_name', 'class_code', 'text']
        if not all(field in request.form for field in required_fields):
            log_message("Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        username = request.form['username']
        password = request.form['password']
        school_name = request.form['school_name']
        class_code = request.form['class_code']
        text = request.form['text']


        # Authenticate user
        auth_status, auth_message = authenticate_user(username, password)
        if not auth_status:
            status_code = 404 if auth_message == 'User not found' else 401
            return jsonify({'error': auth_message}), status_code
        
        # Get file path and save text
        file_path = get_file_path(school_name, class_code, username)
        
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(text + '\n')
            
        log_message(f"TEXT SERVER | Text saved successfully for user: {username}")
        return jsonify({'message': 'Text saved successfully'}), 200
    
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        log_message(f"TEXT SERVER | Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Validate base path exists
    if not os.path.exists(base_path):
        print(f"TEXT SERVER | Base path not found: {base_path}")
        log_message(f"TEXT SERVER | Base path not found: {base_path}")
        exit(1)

    log_message(f"TEXT SERVER | Server started on port {port}")
    debug_stat = False
    with open(request_log_path, 'a') as log_file:
        log_file.write(f'* Serving Flask app "{str(__file__).split('\\')[-1]}"\n* Debug mode: {debug_stat}\n* Running on all addresses (0.0.0.0)\n* Running on http://127.0.0.1:{port}')
        log_file.close()
    app.run(host="0.0.0.0", port=port, debug=debug_stat)