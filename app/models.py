from app import db  # db теперь доступен через этот импорт

class User(db.Model):  # db уже инициализирован
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def get_id(self):
        return str(self.id)  # Возвращаем строковый ID
