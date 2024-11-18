
from backend.extensions import db

class Wallet(db.Model):
    __tablename__ = 'wallet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_cold = db.Column(db.Boolean, default=False)
    crypto = db.Column(db.String(120))
    address = db.Column(db.String(120), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)