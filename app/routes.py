from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required  # Защищает страницу, доступную только авторизованным пользователям
def index():
    return render_template("index.html")
