
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services import WalletService, UserService

wallet_blueprint = Blueprint('wallet', __name__)
wallet_service = WalletService()
user_service = UserService()

@wallet_blueprint.route('/create/hot_wallet', methods=['POST'])
@jwt_required()
def create_hot_wallet():
    username = get_jwt_identity()
    data = request.get_json()
    crypto = data.get('crypto')
    if not crypto:
        return jsonify({'message': 'Cryptocurrency is required'}), 400
    user = user_service.get_user(username)
    wallet = wallet_service.create_wallet(user.id, crypto=crypto, is_cold=False)
    return jsonify({'address': wallet.address}), 201

@wallet_blueprint.route('/create/cold_wallet', methods=['POST'])
@jwt_required()
def create_cold_wallet():
    username = get_jwt_identity()
    data = request.get_json()
    crypto = data.get('crypto')
    if not crypto:
        return jsonify({'message': 'Cryptocurrency is required'}), 400
    user = user_service.get_user(username)
    wallet = wallet_service.create_wallet(user.id, crypto=crypto, is_cold=True)
    return jsonify({'address': wallet.address}), 201

@wallet_blueprint.route('/all_wallets', methods=['GET'])
@jwt_required()
def get_all_wallets():
    username = get_jwt_identity()
    user = user_service.get_user(username)
    wallets = wallet_service.get_all_wallets(user.id)
    dict_wallets = [{'id': wlt.id, 'user_id': wlt.user_id, 'is_cold': wlt.is_cold,
                     'address': wlt.address, 'balance': wlt.balance, 'crypto': wlt.crypto} for wlt in wallets]
    if dict_wallets:
        return jsonify({'wallets': dict_wallets}), 200
    else:
        return jsonify({'message': 'Wallets are not found'}), 404

@wallet_blueprint.route('/remove', methods=['DELETE'])
@jwt_required()
def remove_wallet():
    username = get_jwt_identity()
    data = request.get_json()
    address = data.get('address')
    user = user_service.get_user(username)
    wallet = wallet_service.get_wallet(user.id, address=address)
    wallet_service.remove_wallet(wallet)
    return jsonify({'message': 'Wallet deleted'}), 200