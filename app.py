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
    return "<h1>Login Page</h1>"


@app.route('/register')
def login():
    return "<h1>Registration</h1>"


@app.route('/home')
def listing():
    return "<h1>Listing of Elements</h1>"


@app.route('/profile')
def profile():
    return "<h1>User Profile</h1>"


@app.route('/entry')
def entry():
    return "<h1>Entry</h1>"


@app.route('/add')
def new_entry():
    return "<h1>New Entry</h1>"


if __name__ == '__main__':
    app.run(host=os.environ.get('HOSTNAME'),
            port=int(os.environ.get('PORT')),
            debug=os.environ.get('DEV'))
