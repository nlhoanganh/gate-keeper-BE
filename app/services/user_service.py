import csv
from app.models.user import User
from app.utils.file import save_image
from datetime import datetime

USER_DATA_FILE = 'app/data/users.csv'

#TO-DO: Add roll-back feature when an error happens
def add_user(user: User) -> None:
    with open(USER_DATA_FILE, 'a') as user_file:
        if is_user_existed(user.id):
            raise ValueError(f"User '{user.id}' already exists, name: '{user.name}'")
        else:
            user_file.write(f"\n{user.id},{user.name},{user.email},{user.role}")
            for index, face_image in enumerate(user.face_images, start=1):
                file_name = _generate_user_image_name(user) + "_" + str(index) + ".jpg"
                save_image(face_image, "dataset", file_name)

def is_user_existed(employee_id: str) -> bool:
    with open(USER_DATA_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["id"]) == employee_id:
                return True

    return False

def _generate_user_image_name(user: User) -> str:
    return f"{user.id}_{user.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"