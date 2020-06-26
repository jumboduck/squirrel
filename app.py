import os
from os import path
if path.exists("env.py"):
    import env
from flask import Flask, render_template, url_for, flash, redirect, session
from forms import RegistrationForm, LoginForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')


mongo = PyMongo(app)
bcrypt = Bcrypt(app)


"""
USER MANAGEMENT
"""

# Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    users = mongo.db.users
    if form.validate_on_submit():
        login_user = users.find_one({'username' : form.username.data})
        if login_user and bcrypt.check_password_hash(login_user['password'], form.password.data.encode('utf-8')):
            session["username"] = form.username.data
            flash(f'Welcome to squirrel, {form.username.data}.', 'success')
            return redirect(url_for('listing'))
        else:
            flash('Wrong username or password.', 'danger')

    return render_template('pages/login.html', title="Login", form=form)


# Registration

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    users = mongo.db.users
    if form.validate_on_submit():
        existing_user = users.find_one({'username' : form.username.data})
        existing_email = users.find_one({'email': form.email.data})
        if existing_user is None and existing_email is None:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            users.insert({
                "username": form.username.data,
                "email": form.email.data,
                "password": hashed_password,
            })
            flash(f'Account created for {form.username.data}.', 'success')
            return redirect(url_for('login'))
        elif existing_user:
            flash(f'Username {form.username.data} is already in use.', 'danger')
        elif existing_email:
            flash(f'An account already exists for {form.email.data}.', 'danger')

    return render_template('pages/registration.html', title="Registration", form=form)

# Logout

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash(f'Sucessfully logged out.', 'success')
    return redirect(url_for('login'))


"""
Pages
"""

@app.route('/')
@app.route('/listing')
def listing():
    return render_template('pages/listing.html',  title="Listing", entries=mongo.db.entries.find())


@app.route('/profile')
def profile():
    return render_template('pages/profile.html',  title="Profile")


@app.route('/entry/<entry_id>')
def entry(entry_id):
    the_entry = mongo.db.entries.find_one({"_id": ObjectId(entry_id)})
    return render_template('pages/entry.html',  title="Entry" , entry=the_entry)


@app.route('/add')
def new_entry():
    return render_template('pages/new_entry.html',  title="New Entry")


@app.route('/search')
def search():
    return render_template('pages/search.html',  title="Search")


if __name__ == '__main__':
    app.run(host=os.environ.get('HOSTNAME'),
            port=int(os.environ.get('PORT')),
            debug=os.environ.get('DEV'))
