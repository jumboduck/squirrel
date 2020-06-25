import os
from os import path
if path.exists("env.py"):
    import env
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId



app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'simon' and form.password.data == 'password':
            flash('You are logged in', 'success')
            return redirect(url_for('listing'))
        else:
            flash('Wrong username or password', 'danger')

    return render_template('pages/login.html', title="Login", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}.', 'success')
        return redirect(url_for('listing'))
    return render_template('pages/registration.html', title="Registration", form=form)


@app.route('/')
@app.route('/listing')
def listing():
    return render_template('pages/listing.html',  title="Listing", entries=mongo.db.entries.find())


@app.route('/profile')
def profile():
    return render_template('pages/profile.html',  title="Profile")


@app.route('/entry')
def entry():
    return render_template('pages/entry.html',  title="Entry")


@app.route('/add')
def new_entry():
    return render_template('pages/new_entry.html',  title="New Entry")


@app.route('/search')
def search():
    return render_template('pages/search.html',  title="Search")


@app.route('/logout')
def logout():
    return "<h1>Logout</h1>"


if __name__ == '__main__':
    app.run(host=os.environ.get('HOSTNAME'),
            port=int(os.environ.get('PORT')),
            debug=os.environ.get('DEV'))
