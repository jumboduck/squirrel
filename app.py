from flask import Flask, render_template, url_for, flash, redirect
import os
from os import path
from forms import RegistrationForm, LoginForm
if path.exists("env.py"):
    import env

SECRET_KEY = os.environ.get('SECRET_KEY')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
MONGO_URI = os.environ.get('MONGO_URI')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('pages/login.html', title="Login", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}.', 'success')
        return redirect(url_for('listing'))
    return render_template('pages/registration.html', title="Registration", form=form)


@app.route('/home')
def listing():
    return render_template('pages/listing.html',  title="Listing")


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
