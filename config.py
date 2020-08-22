from flask import Flask
from os import path
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os
import re
if path.exists("env.py"):
    import env


# Initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['CLOUDINARY_URL'] = os.environ.get('CLOUDINARY_URL')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER'] 
app.config['MAIL_USE_SSL'] = os.environ['MAIL_USE_SSL']
app.config['MAIL_PORT'] = os.environ['MAIL_PORT'] 


mongo = PyMongo(app)
bcrypt = Bcrypt(app)
mail = Mail(app)


"""
Global Variables
"""


users = mongo.db.users
entries = mongo.db.entries
time_format = "%d/%m/%Y at %H:%M:%S"
text_regex = re.compile("^[\\S].*")
