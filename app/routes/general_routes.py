from flask import Blueprint, render_template
from flask_login import current_user


general_bp = Blueprint('general', __name__)


@general_bp.route("/")
def index():
    print("Rendering index.html")
    return render_template("index.html", user=current_user)


@general_bp.route("/features")
def features():
    return render_template("general/features.html")


@general_bp.route("/discover")
def discover():
    # For now, we'll use placeholder data
    trending_songs = []  # Replace with actual database query later
    return render_template("general/discover.html",
                         trending_songs=trending_songs,
                         user=current_user)


@general_bp.route("/contact")
def contact():
    return render_template("general/contact.html")
