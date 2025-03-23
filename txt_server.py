from flask import Flask, request, jsonify
import os
import mysql.connector
from mysql.connector import Error
from gevent.pywsgi import WSGIServer
import logging
import configparser
from log_handler import log_message

config_path = os.path.join('config.ini')
config = configparser.ConfigParser()
config.read(config_path)

app = Flask(__name__)

# Configuration 
port = int(config['Server']['txt_server_port'])
BASE_PATH = config['Server']['schools_path']
ALLOWED_APPLICATION = "SchoolApp"
REQUIRED_HEADER = "X-Application"
db_ip_address = config['Database']['Host']
db_name = config['Database']['Database']
db_port = int(config['Database']['DB_port'])
db_user = config['Database']['User']
db_password = config['Database']['Password']

# Database configuration (Use environment variables in production)
DB_CONFIG = {
    'host': db_ip_address,
    'database': db_name,
    'port': db_port,
    'user': db_user,
    'password': db_password
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_application_header():
    """Validate the request contains required application header"""
    app_header = request.headers.get(REQUIRED_HEADER)
    if app_header != ALLOWED_APPLICATION:
        logger.warning(f"Invalid header detected: {app_header}")
        log_message(f"Invalid header detected: {app_header}")
        return False
    return True

def get_user_password(username: str) -> tuple:
    """Retrieve user password and existence status from database"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT student_password FROM students WHERE student_national_code = %s",
                    (username,)
                )
                result = cursor.fetchone()
                if not result:
                    return (False, "User not found")
                return (True, result[0])
    except Error as e:
        logger.error(f"Database error: {str(e)}")
        log_message(f"Database connection error {str(e)}")
        return (False, f"Database connection error {str(e)}")

def validate_directory_path(school: str, class_code: str) -> tuple:
    """Validate the target directory exists"""
    target_path = os.path.join(BASE_PATH, school, class_code)
    if not os.path.exists(target_path):
        logger.error(f"Directory not found: {target_path}")
        log_message(f"Directory not found: {target_path}")
        return (False, "Directory does not exist")
    if not os.access(target_path, os.W_OK):
        logger.error(f"Directory not writable: {target_path}")
        log_message("Directory not writable")
        return (False, "Directory not writable")
    return (True, target_path)

@app.route('/upload_text', methods=['POST'])
def upload_text():
    try:
        # Header validation
        if not validate_application_header():
            log_message("Unauthorized application")
            return jsonify({"error": "Unauthorized application"}), 403

        # Data validation
        required_fields = ['username', 'password', 'school_name', 'class_code', 'text']
        if not all(field in request.form for field in required_fields):
            logger.error("Missing required fields")
            log_message("Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        username = request.form['username']
        password = request.form['password']
        school_name = request.form['school_name']
        class_code = request.form['class_code']
        text = request.form['text']

        logger.info(f"Request received from user: {username}")
        log_message(f"Request received from user: {username}")

        # User existence check
        user_status, db_password = get_user_password(username)
        if not user_status:
            status_code = 404 if db_password == "User not found" else 500
            return jsonify({"error": db_password}), status_code

        # Password validation
        if db_password != password:
            logger.warning(f"Invalid password for user: {username}")
            log_message(f"Invalid password for user: {username}")
            return jsonify({"error": "Authentication failed"}), 401

        # Directory validation
        dir_status, full_path = validate_directory_path(school_name, class_code)
        if not dir_status:
            return jsonify({"error": full_path}), 500

        # Save text to file
        try:
            file_path = os.path.join(full_path, f"{username}.txt")
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(text + '\n')
            logger.info(f"Text saved successfully for user: {username}")
            log_message('Text saved successfully')
            return jsonify({"message": "Text saved successfully"}), 200
        except IOError as e:
            logger.error(f"File write error: {str(e)}")
            log_message("File storage failed")
            return jsonify({"error": "File storage failed"}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        log_message('Internal server error')
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Validate base path exists
    if not os.path.exists(BASE_PATH):
        logger.error(f"Base path not found: {BASE_PATH}")
        log_message(f"Base path not found: {BASE_PATH}")
        exit(1)

    # Start production server
    http_server = WSGIServer(('0.0.0.0', port), app)
    logger.info(f"Starting server on port {port}")
    log_message(f"Starting server on port {port}")
    http_server.serve_forever()