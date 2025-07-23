from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.transaction import Transaction
from app import db
from datetime import datetime

wallet_bp = Blueprint('wallet', __name__)

@wallet_bp.route('/balance', methods=['GET'])
@login_required
def check_balance():
    return jsonify({'balance': current_user.wallet_balance})

@wallet_bp.route('/deposit', methods=['POST'])
@login_required
def deposit():
    data = request.get_json()
    amount = data.get('amount')

    if not amount or amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400

    current_user.wallet_balance += amount

    transaction = Transaction(
        user_id=current_user.id,
        amount=amount,
        type='deposit',
        description='Wallet deposit',
        timestamp=datetime.utcnow()
    )

    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Deposit successful', 'new_balance': current_user.wallet_balance})

@wallet_bp.route('/withdraw', methods=['POST'])
@login_required
def withdraw():
    data = request.get_json()
    amount = data.get('amount')

    if not amount or amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400

    if current_user.wallet_balance < amount:
        return jsonify({'message': 'Insufficient funds'}), 400

    current_user.wallet_balance -= amount

    transaction = Transaction(
        user_id=current_user.id,
        amount=-amount,  # Negative value for withdrawal
        type='withdrawal',
        description='Wallet withdrawal',
        timestamp=datetime.utcnow()
    )

    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Withdrawal successful', 'new_balance': current_user.wallet_balance})

@wallet_bp.route('/transactions', methods=['GET'])
@login_required
def transaction_history():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).all()

    data = [{
        'amount': tx.amount,
        'type': tx.type,
        'description': tx.description,
        'timestamp': tx.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for tx in transactions]

    return jsonify({'transactions': data})
