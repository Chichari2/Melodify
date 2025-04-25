from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
from app.routes import main_bp
from app.models import User
from app.extensions import db

login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    if not user_id:
        return None
    try:
        return db.session.query(User).get(int(user_id))
    except (ValueError, TypeError):
        return None



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Регистрируем blueprint
    app.register_blueprint(main_bp)

    # Инициализируем db, login_manager и csrf в этом месте
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Теперь импортируем модели, чтобы избежать циклических импортов
    with app.app_context():
        from app import models

    # Создаем таблицы в базе данных
    with app.app_context():
        db.create_all()

    return app

