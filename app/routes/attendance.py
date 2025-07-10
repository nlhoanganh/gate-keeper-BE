from flask import Blueprint, request, jsonify, Response
from app.models.user import User
from app.services.user_service import add_user, get_user_from_base64_image
bp = Blueprint('attendance', __name__)

@bp.route('/login', methods=['POST'])
def login():

    data = request.json
    img_base64 = data.get('image')

    verified_user = get_user_from_base64_image(img_base64)

    return jsonify({
        "person": verified_user.to_dict() if verified_user is not None else None,
    })

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    faceImages = data.get('faceImages')
    new_user = User(
        employee_id=data['employee_id'],
        name=data['name'],
        email=data['email']
    )

    new_user.images = faceImages

    # Validate required fields
    required_fields = ['employee_id', 'name', 'email']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

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