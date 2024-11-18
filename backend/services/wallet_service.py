
import secrets

from backend.models import Wallet
from backend.extensions import db

class WalletService:
    def create_wallet(self, user_id: int, crypto: str, is_cold: bool) -> Wallet:
        key = secrets.token_bytes(32)
        address = key.hex()
        wallet = Wallet(user_id=user_id, crypto=crypto, is_cold=is_cold, address=address)
        db.session.add(wallet)
        db.session.commit()
        return wallet

    def get_wallet(self, user_id: int, wallet_id: int = None, address: str = None) -> Wallet:
        if wallet_id:
            return Wallet.query.filter_by(user_id=user_id, wallet_id=wallet_id).first()
        elif address:
            return Wallet.query.filter_by(user_id=user_id, address=address).first()

    def get_all_wallets(self, user_id: int) -> list[Wallet]:
        return Wallet.query.filter_by(user_id=user_id).all()

    def remove_wallet(self, wallet: Wallet):
        db.session.delete(wallet)
        db.session.commit()