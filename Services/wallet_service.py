from models import wallet
from db import db

def init_wallet_service(app):
    pass

def create_hot_wallet(user_id):
    new_wallet = wallet(user_id=user_id, is_cold=False)
    db.session.add(new_wallet)
    db.session.commit()
    return new_wallet

def create_cold_wallet(user_id):
    new_wallet = wallet(user_id=user_id, is_cold=True)
    db.session.add(new_wallet)
    db.session.commit()
    return new_wallet

def get_wallets(user_id):
    return wallet.query.filter_by(user_id=user_id).all()

def get_wallet(user_id, wallet_id):
    return wallet.query.filter_by(user_id=user_id, wallet_id=wallet_id).first()