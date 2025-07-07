from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from deepface import DeepFace
import os
import base64
from datetime import datetime
import json

app = Flask(__name__)

# Thư mục upload
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Thư mục ảnh mẫu
DATASET_PATH = 'dataset'
os.makedirs(DATASET_PATH, exist_ok=True)

# Cấu hình email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'xifintest@gmail.com'
app.config['MAIL_PASSWORD'] = 'rlsjfmivvxckucye'   # Hoặc app password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Ghi log điểm danh
LOG_FILE = 'attendance_log.json'
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

# API Ping
@app.route('/api/ping', methods=['POST'])
def ping():
    data = request.json
    print('Ping:', data)
    return jsonify({"status": "ok"})

# API điểm danh
@app.route('/api/attendance', methods=['POST'])
def attendance():
    data = request.json
    timestamp = data['timestamp']
    img_base64 = data['image']

    # Lưu ảnh
    if "," in img_base64:
        img_base64 = img_base64.split(",")[1]

    filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(base64.b64decode(img_base64))
        print("Đã lưu file:", filepath)
        print("Kích thước file:", os.path.getsize(filepath), "bytes")

    # Nhận diện khuôn mặt
    try:
        result = DeepFace.find(img_path=filepath,
                               db_path=DATASET_PATH,
                               model_name="Facenet",
                               enforce_detection=False)
        if len(result) > 0 and not result[0].empty:
            # result[0] là DataFrame
            best_match = result[0].iloc[0]
            person = os.path.basename(os.path.dirname(best_match["identity"]))
            confidence = round(100 - best_match["distance"]*100, 2)
            matched = True
        else:
            person = None
            confidence = 0
            matched = False

    except Exception as e:
        print("DeepFace error:", e)
        person = None
        confidence = 0
        matched = False

    # Ghi log
    log_entry = {
        "timestamp": timestamp,
        "filename": filename,
        "matched": matched,
        "person": person,
        "confidence": confidence
    }
    with open(LOG_FILE, 'r+') as f:
        logs = json.load(f)
        logs.append(log_entry)
        f.seek(0)
        json.dump(logs, f, indent=2)

    # Gửi email nếu nhận diện thành công
    if matched and person:
        try:
            msg = Message(subject="Thông báo điểm danh",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=["john.nguyen@terralogic.com"],
                          body=f"Nhân viên {person} đã điểm danh lúc {timestamp} (độ tin cậy: {confidence}%).")
            mail.send(msg)
            email_status = "Sent"
        except Exception as e:
            print("Mail error:", e)
            email_status = "Error"
    else:
        email_status = "Skipped"

    return jsonify({
        "matched": matched,
        "person": person,
        "confidence": confidence,
        "email_status": email_status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)