from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Модель User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    # Хэширование пароля
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Проверка пароля
    def check_password(self, password):
        return check_password_hash(self.password, password)
