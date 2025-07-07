from flask_mail import Message
from app import mail
from flask import current_app

def send_attendance_email(person, timestamp, confidence):
    try:
        msg = Message(
            subject="Thông báo điểm danh",
            sender=current_app.config['MAIL_USERNAME'],
            recipients=["john.nguyen@terralogic.com"],
            body=f"Nhân viên {person} đã điểm danh lúc {timestamp} (độ tin cậy: {confidence}%)."
        )
        mail.send(msg)
        return "Sent"
    except Exception as e:
        print("Mail error:", e)
        return "Error"