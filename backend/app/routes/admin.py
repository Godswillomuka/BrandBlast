from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.transaction import Transaction
from app import db
from functools import wraps

admin_bp = Blueprint('admin', __name__)

# ✅ Admin-only route decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


# ✅ View all users
@admin_bp.route('/admin/users', methods=['GET'])
@login_required
@admin_required
def view_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'wallet_balance': user.wallet_balance,
            'is_admin': user.is_admin
        })
    return jsonify({'users': result})


# ✅ View all transactions (wallet and SMS)
@admin_bp.route('/admin/transactions', methods=['GET'])
@login_required
@admin_required
def view_all_transactions():
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    result = []
    for txn in transactions:
        result.append({
            'user_id': txn.user_id,
            'type': txn.txn_type,
            'amount': txn.amount,
            'details': txn.details,
            'timestamp': txn.timestamp.isoformat()
        })
    return jsonify({'transactions': result})


# ✅ Promote user to admin
@admin_bp.route('/admin/promote/<int:user_id>', methods=['PATCH'])
@login_required
@admin_required
def promote_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.is_admin = True
    db.session.commit()
    return jsonify({'message': f'{user.email} promoted to admin'})


# ✅ Suspend user (disable login)
@admin_bp.route('/admin/suspend/<int:user_id>', methods=['PATCH'])
@login_required
@admin_required
def suspend_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.is_active = False
    db.session.commit()
    return jsonify({'message': f'{user.email} has been suspended'})
