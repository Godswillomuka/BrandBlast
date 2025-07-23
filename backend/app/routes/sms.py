from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.transaction import Transaction
from app.utils.helpers import send_sms_message  # abstracted SMS sender
import datetime

sms_bp = Blueprint('sms', __name__)

SMS_COST = 1.00  # Cost per SMS in wallet units (e.g. 1 KES per SMS)

# ✅ Send SMS
@sms_bp.route('/sms/send', methods=['POST'])
@login_required
def send_sms():
    data = request.get_json()
    recipient = data.get('recipient')
    message = data.get('message')

    if not recipient or not message:
        return jsonify({'error': 'Recipient and message required'}), 400

    # Check balance
    if current_user.wallet_balance < SMS_COST:
        return jsonify({'error': 'Insufficient wallet balance'}), 402

    # Send SMS using utility
    success = send_sms_message(recipient, message)

    if success:
        # Deduct wallet
        current_user.wallet_balance -= SMS_COST
        # Save transaction
        sms_txn = Transaction(
            user_id=current_user.id,
            txn_type='sms',
            amount=-SMS_COST,
            details=f"Sent SMS to {recipient}",
            timestamp=datetime.datetime.utcnow()
        )
        db.session.add(sms_txn)
        db.session.commit()

        return jsonify({'message': 'SMS sent successfully'})
    else:
        return jsonify({'error': 'Failed to send SMS'}), 500


# ✅ View Sent SMS History
@sms_bp.route('/sms/history', methods=['GET'])
@login_required
def sms_history():
    transactions = Transaction.query.filter_by(user_id=current_user.id, txn_type='sms').order_by(Transaction.timestamp.desc()).all()
    
    result = []
    for txn in transactions:
        result.append({
            'amount': txn.amount,
            'details': txn.details,
            'timestamp': txn.timestamp.isoformat()
        })
    
    return jsonify({'sms_history': result})
