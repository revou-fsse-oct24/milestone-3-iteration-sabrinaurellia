from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("config")

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register routes (to be added later)
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix="/users")

    return app
