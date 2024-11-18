
from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend.extensions import db, jwt

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)
jwt.init_app(app)

from backend.blueprints import auth_blueprint, wallet_blueprint, trade_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(wallet_blueprint, url_prefix='/wallet')
app.register_blueprint(trade_blueprint, url_prefix='/trade')

with app.app_context():
    db.create_all()