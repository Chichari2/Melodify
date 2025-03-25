from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Database configuration - using absolute path
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_dir = os.path.join(basedir, 'database')
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, 'melodify.db')

    # Create empty file with correct permissions
    if not os.path.exists(db_path):
        with open(db_path, 'w') as f:
            os.chmod(db_path, 0o666)

    app.config.update({
        'SECRET_KEY': 'your-secret-key-here',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_pre_ping': True,
            'connect_args': {
                'timeout': 30,
                'check_same_thread': False,
                'uri': True  # Better path handling
            }
        }
    })

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # IMPORTANT: Import models BEFORE create_all()
    from app.models.user import User

    with app.app_context():
        try:
            # Force table creation
            db.create_all()

            # Verify tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✅ Database created at: {db_path}")
            print(f"✅ Tables created: {tables}")

            if 'user' not in tables:
                raise RuntimeError("User table not created!")

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            # Emergency fallback
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            db.create_all()
            print("⚠️ Using in-memory database as fallback")

    # Rest of your code remains the same...
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth_routes import auth_bp
    from app.routes.general_routes import general_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(general_bp)
    app.register_blueprint(dashboard_bp)

    return app

