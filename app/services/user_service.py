from sqlalchemy.exc import DatabaseError

from app import db
from app.models.user import User
from app.utils.file import save_image
from datetime import datetime

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

def is_user_existed(employee_id: int) -> bool:
    user = User.query.get(employee_id)
    if not user:
        return False
    return True

def _generate_user_image_name(user: User, index: int = -1) -> str:
    if (index < 0):
        return f"{user.employee_id}_{user.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    return f"{user.employee_id}_{user.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{index}.jpg"