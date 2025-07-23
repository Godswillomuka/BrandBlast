from flask_mail import Message
from flask import render_template, current_app
from app import mail

def send_reset_email(user):
    token = user.id  # Simplified; ideally use a token
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    
    msg.body = f'''To reset your password, visit the following link:
{current_app.config['FRONTEND_URL']}/reset-password/{token}

If you did not make this request, simply ignore this email.
'''
    mail.send(msg)

def send_welcome_email(user):
    msg = Message('Welcome to BrandBlast!',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    
    msg.body = f'''Hello {user.name},

Thank you for joining BrandBlast. Start exploring now!

Best,
BrandBlast Team
'''
    mail.send(msg)
