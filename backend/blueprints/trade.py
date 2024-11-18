
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services import TradeService, UserService

trade_blueprint = Blueprint('trade', __name__)
trade_service = TradeService()
user_service = UserService()
