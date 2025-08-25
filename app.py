import os
import base64
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify, render_template

# إخفاء رسائل Info من TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from predict import predict  # استدعاء دالتك الخاصة بالتنبؤ

app = Flask(__name__)

# مجلد التحميل المؤقت
UPLOAD_FOLDER = 'uploads'
TEMP_FILE_NAME = 'temp_upload.jpg'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result_page():
    prediction = request.args.get("prediction", "❌ لا توجد نتيجة")
    return render_template('result.html', prediction=prediction)

@app.route('/camera-predict', methods=['POST'])
def camera_predict():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image data"}), 400

    try:
        # معالجة Base64
        image_data = data['image'].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))

        file_path = os.path.join(UPLOAD_FOLDER, TEMP_FILE_NAME)
        image.save(file_path)

        # التنبؤ من النموذج
        result = predict(file_path)

        # حذف الملف المؤقت بعد التنبؤ
        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# تعديل ليعمل على Render مع Gunicorn
if __name__ == '__main__':
    # أثناء التطوير
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 3000)), debug=False)
