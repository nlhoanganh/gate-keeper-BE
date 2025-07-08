from flask import Flask
from flask_mail import Mail
import os

from flask_sqlalchemy import SQLAlchemy

from .config import Config

mail = Mail()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs('uploads', exist_ok=True)
    os.makedirs('dataset', exist_ok=True)
    os.makedirs('app/logs', exist_ok=True)

    mail.init_app(app)
    db.init_app(app)

    from .routes.attendance import bp as attendance_bp
    app.register_blueprint(attendance_bp, url_prefix='/api')

    return app