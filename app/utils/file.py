import base64
import os
import json
from datetime import datetime


LOG_FILE = 'app/logs/attendance_log.json'
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

def save_image(img_base64, folder_path, file_name = "") -> (str, str):
    if "," in img_base64:
        img_base64 = img_base64.split(",")[1]

    filename = file_name or f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(folder_path, filename)

    with open(filepath, "wb") as f:
        f.write(base64.b64decode(img_base64))
        print("Saved file:", filepath)
        print("File size:", os.path.getsize(filepath), "bytes")

    return filename, filepath

def write_log(entry) -> None:
    with open(LOG_FILE, 'r+') as f:
        logs = json.load(f)
        logs.append(entry)
        f.seek(0)
        json.dump(logs, f, indent=2)

