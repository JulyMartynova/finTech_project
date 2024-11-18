
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from backend.services import UserService

auth_blueprint = Blueprint('auth', __name__)
user_service = UserService()

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, password = data.get('username'), data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    user = user_service.create_user(username, password)
    if not user:
        return jsonify({'message': 'User already exists'}), 400
    return jsonify({'message': 'User registered successfully'}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username, password = data.get('username'), data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    user = user_service.get_user(username)
    if not user or not user_service.verify_user(password, user.password):
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=user.username)
    return jsonify({'access_token': access_token}), 200

@auth_blueprint.route('/verify', methods=['GET'])
@jwt_required()
def verify():
    return jsonify({'message': 'Token is valid'}), 200

