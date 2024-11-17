from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app import create_app

from Services.user_service import create_user, get_user
from Services.wallet_service import create_hot_wallet, create_cold_wallet, get_wallets
from Services.order_book import OrderBook, order
from werkzeug.security import check_password_hash

logger = logging.getLogger(__name__)

bp = Blueprint('routes', __name__)

@bp.route('/register', methods=['POST'])
def register_route():
    try:
        data = request.json
        user = create_user(data['username'], data['password'])
        logger.info(f'User with id {user.id} registered successfully')
        return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201
    except Exception as e:
        logger.error(f'User failed registration: {str(e)}')
        return jsonify({'message': 'User failed registration'}), 500

@bp.route('/login', methods=['POST'])
def login_route():
    try:
        data = request.json
        user = get_user(data['username'])
        if user and check_password_hash(user.password, data['password']):
            token = create_access_token(identity=user.id)
            logger.info(f"User logged in successfully: {user.id}")
            return jsonify({'token': token}), 200
        logger.warning(f"Invalid credentials for user: {data['username']}")
        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({'message': 'Error during login'}), 500

@bp.route('/wallets/create/hot_wallet', methods=['POST'])
@jwt_required()
def create_hot_wallet_route():
    try:
        user_id = get_jwt_identity()
        wallet = create_hot_wallet(user_id)
        logger.info(f"Hot wallet created for user: {user_id}")
        return jsonify({'address': wallet.address}), 201
    except Exception as e:
        logger.error(f"Error creating hot wallet: {str(e)}")
        return jsonify({'message': 'Error creating hot wallet'}), 500

@bp.route('/wallets/create/cold_wallet', methods=['POST'])
@jwt_required()
def create_cold_wallet_route():
    try:
        user_id = get_jwt_identity()
        wallet = create_cold_wallet(user_id)
        logger.info(f"Cold wallet created for user: {user_id}")
        return jsonify({'address': wallet.address}), 201
    except Exception as e:
        logger.error(f"Error creating cold wallet: {str(e)}")
        return jsonify({'message': 'Error creating cold wallet'}), 500

@bp.route('/wallets', methods=['GET'])
@jwt_required()
def get_wallets_route():
    try:
        user_id = get_jwt_identity()
        wallets = get_wallets(user_id)
        if wallets:
            logger.info(f"Wallets retrieved for user: {user_id}")
            return jsonify({'wallets': wallets}), 200
        logger.warning(f"Wallets not found for user: {user_id}")
        return jsonify({'message': 'Wallets are not found'}), 404
    except Exception as e:
        logger.error(f"Error retrieving wallets: {str(e)}")
        return jsonify({'message': 'Error retrieving wallets'}), 500

@bp.route('/order', methods=['POST'])
@jwt_required()
def create_order_route():
    try:
        user_id = get_jwt_identity()
        data = request.json
        if not data or not data.get('wallet_id') or not data.get('type') or not data.get('price') or not data.get('amount'):
            return jsonify({'message': 'Invalid data'}), 400

        order = order(user_id=user_id, wallet_id=data['wallet_id'], type=data['type'], price=data['price'], amount=data['amount'], created_at=datetime.utcnow())

        # Явное управление сессией
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        Session = sessionmaker(bind=engine)
        session = Session()

        session.add(order)
        session.commit()
        session.close()

        OrderBook.add_order(order)
        OrderBook.match_orders()
        logger.info(f"Order created successfully for user: {user_id}")
        return jsonify({'message': 'Order created successfully'}), 201
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        return jsonify({'message': 'Error creating order'}), 500

@bp.route('/order_book', methods=['GET'])
@jwt_required()
def get_order_book_route():
    try:
        table = OrderBook.display_order_book()
        if table:
            logger.info("Order book retrieved successfully")
            return jsonify({'order_book': table}), 200
        logger.warning("Order book not found")
        return jsonify({'message': 'Order book not found'}), 404
    except Exception as e:
        logger.error(f"Error retrieving order book: {str(e)}")
        return jsonify({'message': 'Error retrieving order book'}), 500