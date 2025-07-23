from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import db, User
import os
from werkzeug.utils import secure_filename
from uuid import uuid4

auth_bp = Blueprint('auth', __name__)

UPLOAD_FOLDER = 'app/static/profile_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Upload helper
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    existing = User.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'message': 'Email already exists'}), 409

    hashed_pw = generate_password_hash(data['password'])
    new_user = User(
        full_name=data['full_name'],
        email=data['email'],
        password=hashed_pw
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    login_user(user)
    return jsonify({'message': 'Login successful'}), 200

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    user = current_user
    return jsonify({
        'full_name': user.full_name,
        'email': user.email,
        'profile_picture': user.profile_picture,
        'date_created': user.date_created
    })

@auth_bp.route('/update-profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.form
    user = current_user
    user.full_name = data.get('full_name', user.full_name)
    user.email = data.get('email', user.email)

    # Profile picture upload
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid4().hex}_{filename}"
            file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
            user.profile_picture = unique_filename

    db.session.commit()
    return jsonify({'message': 'Profile updated'}), 200

@auth_bp.route('/change-password', methods=['PUT'])
@login_required
def change_password():
    data = request.json
    user = current_user
    if not check_password_hash(user.password, data['current_password']):
        return jsonify({'message': 'Current password incorrect'}), 400
    user.password = generate_password_hash(data['new_password'])
    db.session.commit()
    return jsonify({'message': 'Password changed'}), 200
