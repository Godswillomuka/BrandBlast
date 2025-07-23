from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from flask_login import login_user, logout_user, current_user, login_required
from app.utils.mailer import send_reset_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'message': 'User already exists'}), 409

    new_user = User(name=data['name'], email=data['email'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    login_user(user)
    return jsonify({'message': 'Logged in successfully'})


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        send_reset_email(user)
    return jsonify({'message': 'Reset link sent if email exists'})


@auth_bp.route('/reset-password/<int:user_id>', methods=['POST'])
def reset_password(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Invalid user'}), 404

    user.set_password(data['password'])
    db.session.commit()
    return jsonify({'message': 'Password reset successful'})


@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = current_user
    return jsonify({
        'name': user.name,
        'email': user.email,
        'wallet_balance': user.wallet_balance,
        'profile_image': user.profile_image,
        'is_admin': user.is_admin
    })

@auth_bp.route('/profile/update', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()

    if 'name' in data:
        current_user.name = data['name']

    if 'email' in data:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != current_user.id:
            return jsonify({'message': 'Email already in use'}), 400
        current_user.email = data['email']

    if 'password' in data:
        current_user.set_password(data['password'])

    if 'profile_image' in data:
        current_user.profile_image = data['profile_image']  # URL or base64 string

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'})

