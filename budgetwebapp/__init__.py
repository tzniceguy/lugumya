from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin



app = Flask(__name__)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



app.config ['SECRET_KEY'] = 'enter your secret key here'
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lugumya.db'


db = SQLAlchemy(app)

from budgetwebapp import routes
from budgetwebapp.models import User
