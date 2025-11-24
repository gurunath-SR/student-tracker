import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key_123'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'gurunath@2004'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'student_tracker'
    MYSQL_CURSORCLASS = 'DictCursor'
