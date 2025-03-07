# instance/config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'your-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'your_database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
