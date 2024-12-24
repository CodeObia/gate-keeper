from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import getpass
import json

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


def save_users(users):
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)


def register(username, password):
    users = load_users()

    users[username] = {"password": password, "username": username}
    save_users(users)

    print("User registered successfully")


user_name = input('Please enter a username:\n')
existing_users = load_users()

while user_name in existing_users:
    existing_users = load_users()
    user_name = input('Username already exists, please enter another username:\n')

user_password = getpass.getpass("Enter password:\n")
password_confirm = getpass.getpass("Confirm password:\n")

while user_password != password_confirm:
    print("Password don't match...")
    user_password = getpass.getpass("Enter password:\n")
    password_confirm = getpass.getpass("Confirm password:\n")

# Hashing passwords during registration
hashed_password = generate_password_hash(user_password)

register(user_name, hashed_password)
