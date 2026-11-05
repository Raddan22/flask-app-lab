import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-lab5'

# Налаштування логування
if not os.path.exists('logs'):
    os.makedirs('logs')
file_handler = RotatingFileHandler('logs/contact.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

from app import views
from app.users.views import users_bp
from app.products.views import products_bp

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)