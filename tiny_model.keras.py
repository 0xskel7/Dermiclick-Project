import base64, zipfile, io

# هذا النص هو الملف مضغوط Base64
data = '''
UEsDBBQAAAAIAOe...إلخ (سيكون هنا النص الطويل)
'''

# تحويل Base64 إلى بايتات
zip_bytes = base64.b64decode(data.encode('utf-8'))

# فك الضغط وإنشاء الملفات
with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zf:
    zf.extractall(".")

print("✅ تم استخراج tiny_model.keras")
