
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import User
from backend.extensions import db

class UserService:
    def get_user(self, username: str) -> User:
        return User.query.filter_by(username=username).first()

    def create_user(self, username: str, password: str) -> User:
        if self.get_user(username):
            return None
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user

    def verify_user(self, password: str, hashed_password: str) -> bool:
        return check_password_hash(hashed_password, password)