
from backend.models import Trade
from backend.extensions import db

class TradeService:
    def create_trade(self, user_id: int, wallet_id: int, crypto: str, amount: int) -> Trade:
        trade = Trade(user_id=user_id, wallet_id=wallet_id, crypto=crypto, amount=amount)
        db.session.add(trade)
        db.session.commit()
        return trade

    def get_trade(self, user_id: int, wallet_id: int = None) -> Trade:
        return Trade.query.filter_by(user_id=user_id, wallet_id=wallet_id).first()

    def remove_trade(self, trade: Trade):
        db.session.delete(trade)
        db.session.commit()