# INIT
# - this file initializes the flask app and sets up the background task
#   to scrape the fight odds

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
import os

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)
admin = Admin(app)
