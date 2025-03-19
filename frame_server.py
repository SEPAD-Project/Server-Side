from flask import Flask, request, jsonify
import cv2
import os

app = Flask(__name__)

@app.route('/get_student_image', methods=['POST'])
def get_student_image():
    data = request.json
    school_code = data.get('school_code')
    class_name = data.get('class_name')
    national_code = data.get('national_code')

    image_path = f"C://sap-project//{school_code}//{class_name}//{national_code}.jpg"

    if not os.path.exists(image_path):
        return jsonify({'error': 'Image, not found'}), 404
    
    image = cv2.imread(image_path)

    if image is None:
        return jsonify({'error': 'Falid to read image'}), 500
    
    # converting image to byte
    _, image_encoded = cv2.imencode('.jpg', image)
    img_bytes = image_encoded.tobytes()

    return img_bytes, 200, {'Content-Type': 'image/jepg'}

if __name__ == '__main__' : 
    app.run(host='localhost', port=5510, debug=True)