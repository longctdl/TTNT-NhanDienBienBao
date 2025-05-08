# ===== BACKEND: Flask API (app.py) =====
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS 

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

model = load_model('model/traffic_sign_cnndd.keras')


labels = [
    "Speed limit (20km/h)", "Speed limit (30km/h)", "Speed limit (50km/h)", 
    "Speed limit (60km/h)", "Speed limit (70km/h)", "Speed limit (80km/h)", 
    "End of speed limit (80km/h)", "Speed limit (100km/h)", "Speed limit (120km/h)", 
    "No passing", "No passing for vehicles over 3.5 metric tons", "Right-of-way at the next intersection", 
    "Priority road", "Yield", "Stop", "No vehicles", "Vehicles over 3.5 metric tons prohibited", 
    "No entry", "General caution", "Dangerous curve to the left", "Dangerous curve to the right", 
    "Double curve", "Bumpy road", "Slippery road", "Road narrows on the right", 
    "Road work", "Traffic signals", "Pedestrians", "Children crossing", 
    "Bicycles crossing", "Beware of ice/snow", "Wild animals crossing", 
    "End of all speed and passing limits", "Turn right ahead", "Turn left ahead", 
    "Ahead only", "Go straight or right", "Go straight or left", "Keep right", 
    "Keep left", "Roundabout mandatory", "End of no passing", 
    "End of no passing by vehicles over 3.5 metric tons"
]

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3001"}})
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_sign(image_path):
    # Load ảnh và resize
    img = Image.open(image_path).resize((32, 32))
    img_array = np.array(img).astype('float32') / 255.0

    # Nếu ảnh có kênh alpha (RGBA), loại bỏ alpha channel
    if img_array.shape[-1] == 4:
        img_array = img_array[..., :3]

    # Nếu ảnh grayscale (chỉ có 2 chiều), thêm kênh thứ 3
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array]*3, axis=-1)

    # Thêm batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    # Dự đoán
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction)
    return labels[predicted_class]


@app.route('/api/predict', methods=['POST'])
def predict():
    file = request.files.get('image')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Gọi hàm predict_sign của bạn để xử lý ảnh
        label = predict_sign(file_path)
        if label:
            return jsonify({"label": label})  # Trả về kết quả dự đoán
        else:
            return jsonify({"label": "Error processing image"}), 500
    return jsonify({"label": "Invalid file format"}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
