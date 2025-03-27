from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from urllib.parse import urlparse

# Инициализация расширений
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
  app = Flask(__name__)

  # Конфигурация для PostgreSQL на Render
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-key')

  # Получаем URL базы данных из переменных окружения
  db_url = os.getenv('DATABASE_URL', '')

  if db_url:
    # Исправляем URL для SQLAlchemy 2.0+
    if db_url.startswith('postgres://'):
      db_url = db_url.replace('postgres://', 'postgresql://', 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    # Правильная конфигурация для PostgreSQL
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
      'pool_pre_ping': True,
      'connect_args': {
        'connect_timeout': 10  # Таймаут только для PostgreSQL
      }
    }
  else:
    # Fallback для локальной разработки
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///melodify.db'
    # Для SQLite другие параметры
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
      'pool_pre_ping': True
    }

  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  # Инициализация расширений
  db.init_app(app)
  login_manager.init_app(app)

  # Импорт моделей ДО создания таблиц
  from app.models.user import User

  with app.app_context():
    try:
      db.create_all()
      print(f"✅ Подключено к: {app.config['SQLALCHEMY_DATABASE_URI']}")
      # Новый способ получения имен таблиц для SQLAlchemy 2.0
      inspector = db.inspect(db.engine)
      tables = inspector.get_table_names()
      print(f"✅ Таблицы: {tables}")
    except Exception as e:
      print(f"❌ Ошибка БД: {str(e)}")
      if not db_url:  # Только для SQLite fallback
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()
        print("⚠️ Использую SQLite в памяти")

  # Flask-Login
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  @app.route('/db-check')
  def db_check():
    try:
      db.session.execute('SELECT 1')
      return f"Database OK. Using: {db.engine.url}", 200
    except Exception as e:
      return f"Database error: {str(e)}", 500


  # Регистрация компонентов
  from app.routes.auth_routes import auth_bp
  from app.routes.general_routes import general_bp
  from app.routes.dashboard_routes import dashboard_bp

  app.register_blueprint(auth_bp)
  app.register_blueprint(general_bp)
  app.register_blueprint(dashboard_bp)

  return app