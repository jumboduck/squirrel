from flask import Flask, render_template
import os
from os import path
if path.exists("env.py"):
    import env
SECRET_KEY = os.environ.get('SECRET_KEY')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
MONGO_URI = os.environ.get('MONGO_URI')


app = Flask(__name__)


@app.route('/')
@app.route('/login')
def hello_world():
    return render_template('pages/login.html')


@app.route('/register')
def login():
    return render_template('pages/registration.html')


@app.route('/home')
def listing():
    return render_template('pages/listing.html')


@app.route('/profile')
def profile():
    return render_template('pages/profile.html')


@app.route('/entry')
def entry():
    return render_template('pages/entry.html')


@app.route('/add')
def new_entry():
    return render_template('pages/new_entry.html')


@app.route('/search')
def search():
    return render_template('pages/search.html')


@app.route('/logout')
def logout():
    return "<h1>Logout</h1>"


if __name__ == '__main__':
    app.run(host=os.environ.get('HOSTNAME'),
            port=int(os.environ.get('PORT')),
            debug=os.environ.get('DEV'))
