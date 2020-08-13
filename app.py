from os import path
from flask import Flask, render_template, url_for, flash, redirect,\
    request
from forms import RegistrationForm, LoginForm, EntryForm, NewEntryForm, UpdateAccount
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required,\
    logout_user, current_user
from is_safe_url import is_safe_url
from datetime import datetime
from config import app, time_format, entries, users
import login
import update
import routes
import cloudinary
import cloudinary.uploader
import cloudinary.api
import math
import os
import socket



if __name__ == '__main__':
    app.run(host=os.environ.get('HOSTNAME'),
            port=int(os.environ.get('PORT')),
            debug=os.environ.get('DEV'))
