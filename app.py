from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import logging
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
app.logger.info("Flask app is running")

# Secret key for session management
load_dotenv()
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# get the app URL prefix
authenticator_url_prefix = os.environ.get('AUTHENTICATOR_PREFIX')

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User database file
USER_DB_FILE = './users.json'


# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


# Load user data from JSON file
def load_users():
    with open(USER_DB_FILE, 'r') as f:
        return json.load(f)


# Write user data to JSON file
def save_users(users):
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)


# Load user by ID (for session persistence)
@login_manager.user_loader
def load_user(user_id):
    users = load_users()
    if user_id in users:
        return User(user_id, users[user_id]['username'])
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        redirect_url = request.form.get('redirect_url')

        # Authenticate user
        users = load_users()
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(username, users[username]['username'])
            login_user(user)
            return redirect(redirect_url)
        message = 'Invalid credentials'
    else:
        redirect_url = request.headers.get('X-Original-URI', '/')
    return render_template('login.html', redirect_url=redirect_url, message=message, login_url_prefix=authenticator_url_prefix)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/' + AUTHENTICATOR_PREFIX + '/login')


@app.route('/validate', methods=['GET'])
def validate():
    if current_user.is_authenticated:
        return "OK", 200
    else:
        return "Unauthorized", 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
