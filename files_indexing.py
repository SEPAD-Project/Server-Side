from flask import Flask, request, jsonify
import os 
import configparser

config_path = os.path.join(os.path.dirname(__file__), '../config.ini')
config = configparser.ConfigParser()
config.read(config_path)

base_path = config['Server']['schools_path']
port = config['Server']['file_indexing_port']

app = Flask(__name__)


# API for getting students list
@app.route('/get_students', methods=['POST'])
def get_students():
    data = request.get_json()
    school_name = data.get("school_name")
    class_code = data.get("class_code")

    class_path = os.path.join(base_path, school_name, class_code)
    student_list_file = os.path.join(class_path, f"students{class_code}{school_name}.txt")

    if not os.path.exists(student_list_file):
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
    print(class_path)
    if not os.path.exists(class_path):
        return jsonify({"error": "class not found"}), 404

    if not os.path.exists(student_file):
        return jsonify({"error": "Student not found"}), 404

    with open(student_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    last_message = lines[-1].strip() if lines else "No messages yet"
    
    return jsonify({"student": student_name, "message": last_message})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
