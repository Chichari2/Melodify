from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm


app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if request.method == "POST":
        print("Received form data:", request.form)  # Debugging: Check what is submitted

    if form.validate_on_submit():
        print("✅ Form is valid!")

        # Check if the username already exists
        existing_username = db.session.execute(
            db.select(User).filter_by(username=form.username.data)
        ).scalar_one_or_none()

        if existing_username:
            flash('❌ Username already exists. Please choose another one.', 'danger')
            print("❌ Username already exists:", form.username.data)  # Debugging
            return redirect(url_for('register'))

        # Check if the email already exists
        existing_email = db.session.execute(
            db.select(User).filter_by(email=form.email.data)
        ).scalar_one_or_none()

        if existing_email:
            flash('❌ Email address already exists. Use another email.', 'danger')
            print("❌ Email already exists:", form.email.data)  # Debugging
            return redirect(url_for('register'))

        # Hash the password and create the new user
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log the user in
        login_user(new_user)
        session['username'] = new_user.username

        flash("✅ Registration successful!", "success")
        return redirect(url_for('index'))
    else:
        print("❌ Form has errors:", form.errors)  # Debugging validation errors

    return render_template('general/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            session['username'] = user.username
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('auth/login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/")
def index():
    return render_template("index.html", user=current_user)

@app.route("/features")
def features():
    return render_template("general/features.html")

@app.route("/pricing")
def pricing():
    return render_template("general/pricing.html")

@app.route("/contact")
def contact():
    return render_template("general/contact.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)

