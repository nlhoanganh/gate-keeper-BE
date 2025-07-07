from deepface import DeepFace
import os

def recognize_face(filepath):
    try:
        result = DeepFace.find(img_path=filepath, db_path='dataset', model_name="Facenet", enforce_detection=False)
        if len(result) > 0 and not result[0].empty:
            best_match = result[0].iloc[0]
            person = os.path.basename(os.path.dirname(best_match["identity"]))
            confidence = round(100 - best_match["distance"] * 100, 2)
            return True, person, confidence
        else:
            return False, None, 0
    except Exception as e:
        print("DeepFace error:", e)
        return False, None, 0