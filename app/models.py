from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# model for user = email, passwordhash
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    def __repr__(self):
        return '<User {}>'.format(self.username)
    # functions to set a password hash and checks password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)