import os
import base64, zipfile, io
from flask import Flask, request, jsonify, render_template
from PIL import Image
from predict import predict

# إخفاء رسائل TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# -------------------
# فك ضغط النموذج من Base64
# -------------------
data = '''
UEsDBBQAAAAIAOe...إلخ (ضع النص الكامل هنا)
'''
zip_bytes = base64.b64decode(data.encode('utf-8'))
import zipfile, io
with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zf:
    zf.extractall(".")  # سيتم استخراج tiny_model.keras في نفس المجلد
print("✅ تم استخراج tiny_model.keras")

# -------------------
# تحميل النموذج بعد التأكد من وجوده
# -------------------
import tensorflow as tf
model_path = "tiny_model.keras"
if not os.path.exists(model_path):
    raise FileNotFoundError("❌ الملف tiny_model.keras غير موجود بعد الاستخراج!")

model = tf.keras.models.load_model(model_path)
# -------------------

app = Flask(__name__)
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
        image_data = data['image'].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        file_path = os.path.join(UPLOAD_FOLDER, TEMP_FILE_NAME)
        image.save(file_path)
        # التنبؤ باستخدام النموذج
        result = predict(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({"prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 3000)), debug=False)
