from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
from app.routes import main_bp
from app.models import User


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None
    try:
        return User.query.get(int(user_id))
    except (ValueError, TypeError):
        return None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(main_bp)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()  # Create database tables if they don't exist

    return app
