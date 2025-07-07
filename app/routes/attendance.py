from flask import Blueprint, request, jsonify, Response
from app.models.user import User
from app.services.face_regconition_service import recognize_face
from app.utils.email import send_attendance_email
from app.utils.file import save_image, write_log
from app.services.user_service import add_user

bp = Blueprint('attendance', __name__)

@bp.route('/verify-face', methods=['POST'])
def attendance():
    data = request.json
    timestamp = data.get('timestamp')
    img_base64 = data.get('image')

    filename, filepath = save_image(img_base64, "uploads")
    matched, person, confidence = recognize_face(filepath)

    log_entry = {
        "timestamp": timestamp,
        "filename": filename,
        "matched": matched,
        "person": person,
        "confidence": confidence
    }
    write_log(log_entry)

    if matched and person:
        email_status = send_attendance_email(person, timestamp, confidence)
    else:
        email_status = "Skipped"

    return jsonify({
        "matched": matched,
        "person": person,
        "confidence": confidence,
        "email_status": email_status
    })

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    id = data.get('id')
    name = data.get('name')
    email = data.get('email')
    role = data.get('role')
    faceImages = data.get('faceImages')
    new_user = User(id, name, email, role)
    new_user.face_images = faceImages

    try:
        add_user(new_user)
        status_code = 201
        response_message = "User registered successfully"
    except ValueError as e:
        print("Add user failed:", e)
        status_code = 409
        response_message = "User exists"
    except Exception as e:
        print("Add user failed:", e)
        status_code = 500
        response_message = "Failed to add user"

    return jsonify({"status": response_message}), status_code



@bp.route('/ping', methods=['POST'])
def ping():
    data = request.json
    print('Ping:', data)
    return jsonify({"status": "ok"})