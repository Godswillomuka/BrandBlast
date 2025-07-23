from flask import Blueprint

# Import blueprints
from .auth import auth_bp
from .wallet import wallet_bp
from .sms import sms_bp
from .admin import admin_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(wallet_bp, url_prefix='/api/wallet')
    app.register_blueprint(sms_bp, url_prefix='/api/sms')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
