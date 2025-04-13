from flask import Flask, request, jsonify, make_response
import cv2
import os
import configparser
import time 
from datetime import datetime
from pathlib import Path

config_path = os.path.join('../config.ini')
config = configparser.ConfigParser()
config.read(config_path)

port = int(config['Server']['frame_server_port'])
base_path = config['Server']['schools_path']
request_log_path = Path("../"+str(config['ControlServer']['api2_log']))

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

# Handler for wrong methods (405 Method Not Allowed)
@app.errorhandler(405)
def method_not_allowed(error):
    log_message("FRAME SERVER | Wrong method. Please use POST.")
    return jsonify({"error": "Wrong method. Please use POST."}), 405

# Main handler for POST requests
@app.route('/get_student_image', methods=['POST'])
def get_student_image():
    try:
        # Get input data from the user
        data = request.json
        if not data:
            log_message("FRAME SERVER | No input data provided.")
            return jsonify({"error": "No input data provided"}), 400

        school_code = data.get('school_code')
        class_name = data.get('class_name')
        national_code = data.get('national_code')

        # Check if all required fields are present
        if not all([school_code, class_name, national_code]):
            log_message("FRAME SERVER | Missing required fields (school_code, class_name, national_code).")
            return jsonify({"error": "Missing required fields (school_code, class_name, national_code)"}), 400

        # Build the school directory path
        school_dir = f"{base_path}/{school_code}"
        if not os.path.exists(school_dir):
            log_message("FRAME SERVER | School not found.")
            return jsonify({"error": "School not found"}), 404

        # Build the class directory path
        class_dir = os.path.join(school_dir, class_name)
        if not os.path.exists(class_dir):
            log_message("FRAME SERVER | Class not found.")
            return jsonify({"error": "Class not found"}), 404

        # Build the student image file path
        image_path = os.path.join(class_dir, f"{national_code}.jpg")
        if not os.path.exists(image_path):
            log_message("FRAME SERVER | Student image not found.")
            return jsonify({"error": "Student image not found"}), 404

        # Read the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            log_message("FRAME SERVER | Failed to read the image file.")
            return jsonify({"error": "Failed to read the image file"}), 500

        # Convert the image to a byte format for API response
        _, img_encoded = cv2.imencode('.jpg', image)
        img_bytes = img_encoded.tobytes()

        # Return the image as the API response
        return img_bytes, 200, {'Content-Type': 'image/jpeg'}

    except Exception as e:
        # Handle unexpected errors
        log_message(f"FRAME SERVER | An unexpected error occurred: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    log_message(f"FRAME SERVER | Server started on port {port}")
    debug_stat = False
    with open(request_log_path, 'a') as log_file:
        log_file.write(f'* Serving Flask app "{str(__file__).split('\\')[-1]}"\n* Debug mode: {debug_stat}\n* Running on all addresses (0.0.0.0)\n* Running on http://127.0.0.1:{port}')
        log_file.close()
    app.run(host="0.0.0.0", port=port, debug=debug_stat)