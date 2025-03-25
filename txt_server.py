import os
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
import mysql.connector
from mysql.connector import Error
import configparser
from log_handler import log_message

# Configuration setup
config_path = os.path.join('config.ini')
config = configparser.ConfigParser()
config.read(config_path)

app = Flask(__name__)

# Server configuration
port = int(config['Server']['txt_server_port'])
base_path = config['Server']['schools_path']
allowed_application = "SchoolApp"
required_header = "X-Application"

# Database configuration
db_config = {
    'host': config['Database']['Host'],
    'database': config['Database']['Database'],
    'port': int(config['Database']['DB_port']),
    'user': config['Database']['User'],
    'password': config['Database']['Password']
}

def validate_application_header():
    """Validate the request contains required application header"""
    app_header = request.headers.get(required_header)
    if app_header != allowed_application:
        log_message(f"TEXT SERVER | Invalid header detected: {app_header}")
        raise BadRequest('Unauthorized application')

def validate_parameters(request):
    """Validate required parameters in request"""
    required = ['username', 'password', 'school_name', 'class_code', 'text']
    if not all(key in request.form for key in required):
        log_message("TEXT SERVER | Missing required parameters")
        raise BadRequest('Missing required parameters')

def authenticate_user(username, password):
    """Authenticate user against database"""
    try:
        with mysql.connector.connect(**db_config) as connection:
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
        log_message(f"TEXT SERVER | Base path not found: {base_path}")
        exit(1)

    log_message(f"TEXT SERVER | Server started on port {port}")
    app.run(host='0.0.0.0', port=port, threaded=True)