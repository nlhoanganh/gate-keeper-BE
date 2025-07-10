from deepface import DeepFace
import re

def recognize_face(filepath):
    try:
        result = DeepFace.find(img_path=filepath, db_path='dataset', model_name="Facenet", enforce_detection=False)
        if len(result) > 0 and not result[0].empty:
            best_match = result[0].iloc[0]
            user_id = extract_id_from_image(best_match["identity"])
            confidence = round(100 - best_match["distance"] * 100, 2)
            return True, user_id, confidence
        else:
            return False, None, 0
    except Exception as e:
        print("DeepFace error:", e)
        return False, None, 0

def extract_id_from_image(image_path) -> int or None:
    match = re.search(r"(\d+)_", image_path)
    if match:
        return int(match.group(1))
    return -1