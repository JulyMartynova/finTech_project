from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import logging
from dotenv import load_dotenv
from db import db
import os

class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)

load_dotenv()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Проверка наличия необходимых переменных окружения
    if not os.getenv('DATABASE_URL'):
        raise ValueError("DATABASE_URL environment variable is not set")
    if not os.getenv('JWT_SECRET_KEY'):
        raise ValueError("JWT_SECRET_KEY environment variable is not set")

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    # Импортируем и регистрируем Blueprint
    from routes import bp
    app.register_blueprint(bp)

    # Инициализация сервисов и моделей
    from Services import init_services
    init_services(app)

    return app