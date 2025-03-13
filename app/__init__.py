from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Register Blueprints for routing
    from .routes.user_routes import user_bp
    from .routes.account_routes import account_bp
    from .routes.transaction_routes import transaction_bp

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(account_bp, url_prefix="/accounts")
    app.register_blueprint(transaction_bp, url_prefix="/transactions")

    return app
