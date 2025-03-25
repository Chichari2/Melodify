from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print("👥 Users in database:", users)
