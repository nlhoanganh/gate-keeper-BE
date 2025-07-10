from app.services.face_regconition_service import recognize_face
from app.utils.email import send_attendance_email
from app.utils.file import save_image, write_log
from app.utils.worker import execute_job
from app import db
from app.models.user import User
from datetime import datetime, timezone

USER_DATA_FILE = 'app/data/users.csv'

#TO-DO: Add roll-back feature when an error happens
def add_user(user: User) -> None:
    if is_user_existed(user.employee_id):
        raise ValueError(f"User '{user.employee_id}' already exists, name: '{user.name}'")
    else:
        try:
           for index, image_base64 in enumerate(user.images):
               save_image(image_base64, "dataset", _generate_user_image_name(user, index))
           db.session.add(user)
           db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def get_user_from_base64_image(img_base64: str) -> User:
    filename, filepath = save_image(img_base64, "uploads")
    matched, user_id, confidence = recognize_face(filepath)
    verified_user = None
    try:
        verified_user = User.query.filter_by(employee_id=user_id).first()
    except Exception:
        print("User not found, ID: ", user_id)
        
    time_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "matched": matched,
        "confidence": confidence,
        "time": time_str
    }

    if verified_user:
        execute_job(job=send_attendance_email, parameters=(verified_user.name, time_str, confidence))
        log_entry["person"] = verified_user.name
    else:
        log_entry["person"] = None

    execute_job(job=write_log, parameters=(log_entry,))

    return verified_user
    
def is_user_existed(employee_id: int) -> bool:
    user = User.query.get(employee_id)
    if not user:
        return False
    return True

def _generate_user_image_name(user: User, index: int = -1) -> str:
    if (index < 0):
        return f"{user.employee_id}_{user.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    return f"{user.employee_id}_{user.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{index}.jpg"