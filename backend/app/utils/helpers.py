import os
import secrets
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_profile_picture(file):
    """Save profile picture to static/profile_pics/ and return filename."""
    if file and allowed_file(file.filename):
        random_hex = secrets.token_hex(8)
        _, ext = os.path.splitext(file.filename)
        filename = secure_filename(random_hex + ext)
        filepath = os.path.join(current_app.root_path, 'static', 'profile_pics', filename)
        file.save(filepath)
        return filename
    return None

def send_sms_message(recipient, message):
    """Simulated SMS sender (replace with real API integration)."""
    print(f"Sending SMS to {recipient}: {message}")
    # Integrate with a real SMS gateway like Twilio or Africa's Talking
    return True  # Simulate success
