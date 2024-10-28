import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "your_secret_key"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.yourmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your-email@example.com'
    MAIL_PASSWORD = 'your-email-password'
