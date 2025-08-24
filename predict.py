import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# تحميل النموذج
model = tf.keras.models.load_model('my_model.keras')

def predict(img_path):
    """تنبؤ بالصورة وإرجاع النتيجة كنص"""
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.0  # تطبيع الصورة

    preds = model.predict(x)
    if preds[0] > 0.5:
        return "Malignant"
    else:
        return "Benign"

# اختياري: للتشغيل المباشر من التيرمنال
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python predict.py path_to_image.jpg")
    else:
        img_path = sys.argv[1]
        print(f"Prediction: {predict(img_path)}")

