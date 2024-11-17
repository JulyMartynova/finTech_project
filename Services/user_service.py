from werkzeug.security import generate_password_hash, check_password_hash
from models import user
from db import db

def init_user_service(app):
    pass

def create_user(username, password):
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = user(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

def get_user(username):
        return user.query.filter_by(username=username).first()