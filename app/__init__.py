from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from urllib.parse import urlparse  # Для анализа URL

# Инициализация расширений
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
  app = Flask(__name__)

  # Конфигурация для PostgreSQL на Render
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-key')

  # Автоматическая обработка URL от Render
  db_url = os.getenv('DATABASE_URL', '')
  if db_url:
    if db_url.startswith('postgres://'):
      db_url = db_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
  else:
    # Fallback для локальной разработки
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///melodify.db'

  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'connect_timeout': 30
  }

  # Инициализация расширений
  db.init_app(app)
  login_manager.init_app(app)

  # Импорт моделей ДО создания таблиц
  from app.models.user import User

  with app.app_context():
    try:
      db.create_all()
      print(f"✅ Подключено к: {app.config['SQLALCHEMY_DATABASE_URI']}")
      print(f"✅ Таблицы: {db.engine.table_names()}")
    except Exception as e:
      print(f"❌ Ошибка БД: {str(e)}")
      if 'postgresql' not in db_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()
        print("⚠️ Использую SQLite в памяти")

  # Flask-Login
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  # Регистрация компонентов
  from app.routes.auth_routes import auth_bp
  from app.routes.general_routes import general_bp
  from app.routes.dashboard_routes import dashboard_bp

  app.register_blueprint(auth_bp)
  app.register_blueprint(general_bp)
  app.register_blueprint(dashboard_bp)

  return app