from flask import Flask
from os import path
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import os
import re
if path.exists("env.py"):
    import env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['CLOUDINARY_URL'] = os.environ.get('CLOUDINARY_URL')


mongo = PyMongo(app)
bcrypt = Bcrypt(app)


"""
Global Variables
"""


users = mongo.db.users
entries = mongo.db.entries
time_format  = "%d/%m/%Y at %H:%M:%S"
text_regex = re.compile("^[\\S].*")