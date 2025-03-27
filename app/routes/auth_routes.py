from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User
from urllib.parse import urlparse
from app.forms.contact_form import ContactForm
from app.forms import RegistrationForm, LoginForm


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('general.index'))

    form = RegistrationForm()

    if request.method == "POST":
        print("✅ Received form data:", request.form)  # Check received data

    if form.validate_on_submit():
        print("✅ Form is valid!")

        existing_username = db.session.execute(
            db.select(User).filter_by(username=form.username.data)
        ).scalar_one_or_none()

        if existing_username:
            flash('❌ Username already exists. Please choose another one.', 'danger')
            print("⚠️ Username already exists:", existing_username.username)
            return redirect(url_for('auth.register'))

        existing_email = db.session.execute(
            db.select(User).filter_by(email=form.email.data)
        ).scalar_one_or_none()

        if existing_email:
            flash('❌ Email address already exists. Use another email.', 'danger')
            print("⚠️ Email already exists:", existing_email.email)
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            print("✅ User registered successfully:", new_user)
        except Exception as e:
            db.session.rollback()
            print("❌ Database error:", e)

        login_user(new_user)
        session['username'] = new_user.username
        flash("✅ Registration successful!", "success")
        return redirect(url_for('general.index'))

    print("❌ Form validation failed:", form.errors)
    return render_template('general/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            session['username'] = user.username

            # Check the next parameter for redirection
            next_page = request.args.get('next')
            if not next_page or not urlparse(next_page).netloc:  # Avoid external redirects
                next_page = url_for('general.index')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('general.index'))
