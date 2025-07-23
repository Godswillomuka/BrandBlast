import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-dev-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///brandblast.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "backend/static")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
