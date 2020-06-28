import os
from os import path
if path.exists("env.py"):
    import env
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from is_safe_url import is_safe_url
import socket

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')


mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

login_manager.init_app(app)



"""
USER MANAGEMENT
"""

class User(UserMixin):
    def __init__(self, user):
        self.user = user

    def get_id(self):
        object_id = self.user['_id']
        return str(object_id)



@login_manager.user_loader
def load_user(user_id):
    user =  mongo.db.users.find_one({'_id' : ObjectId(user_id)})
    return User(user)


# Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('listing'))
    form = LoginForm()
    users = mongo.db.users
    if form.validate_on_submit():
        user = users.find_one({'email' : form.email.data})
        if user and bcrypt.check_password_hash(user['password'], form.password.data.encode('utf-8')):
            username = user['username']
            login_user(User(user), remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome to squirrel, {username}.', 'success')
            if next_page and is_safe_url(next_page, socket.gethostname()):
                return redirect(next_page)
            else:
                return redirect(url_for('listing'))
        else:
            flash('Login unsucessful, please check email and password.', 'danger')

    return render_template('pages/login.html', title="Login", form=form)


# Registration

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('listing'))
    form = RegistrationForm()
    users = mongo.db.users
    if form.validate_on_submit():
        existing_email = users.find_one({'email': form.email.data})
        if existing_email is None:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            users.insert({
                "username": form.username.data,
                "email": form.email.data,
                "password": hashed_password,
            })
            flash(f'Account created for {form.username.data}.', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'Something went wrong with the information provided.', 'danger')

    return render_template('pages/registration.html', title="Registration", form=form)

# Logout

@app.route('/logout')
def logout():
    logout_user()
    flash(f'Sucessfully logged out.', 'success')
    return redirect(url_for('login'))


"""
Pages
"""

@app.route('/')
@app.route('/listing')
@login_required
def listing():
    return render_template('pages/listing.html',  title="Listing", entries=mongo.db.entries.find())


@app.route('/profile')
@login_required
def profile():
    return render_template('pages/profile.html',  title="Profile")


@app.route('/entry/<entry_id>')
@login_required
def entry(entry_id):
    the_entry = mongo.db.entries.find_one({"_id": ObjectId(entry_id)})
    return render_template('pages/entry.html',  title="Entry" , entry=the_entry)


@app.route('/add')
@login_required
def new_entry():
    return render_template('pages/new_entry.html',  title="New Entry")


@app.route('/search')
@login_required
def search():
    return render_template('pages/search.html',  title="Search")


if __name__ == '__main__':
    app.run(host=os.environ.get('HOSTNAME'),
            port=int(os.environ.get('PORT')),
            debug=os.environ.get('DEV'))
