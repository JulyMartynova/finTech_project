from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_services(app):
    from .user_service import init_user_service
    from .wallet_service import init_wallet_service
    from .order_book import init_order_book

    init_user_service(app)
    init_wallet_service(app)
    init_order_book(app)