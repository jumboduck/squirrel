import os
from os import path
if path.exists("env.py"):
    import env
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from forms import RegistrationForm, LoginForm, EntryForm, NewEntryForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from is_safe_url import is_safe_url
import socket
from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['CLOUDINARY_URL'] = os.environ.get('CLOUDINARY_URL')


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
        self.username = user['username']
        self.id = user['_id']

    def get_id(self):
        object_id = self.user['_id']
        return str(object_id)



@login_manager.user_loader
def load_user(user_id):
    user =  mongo.db.users.find_one({'_id' : ObjectId(user_id)})
    return User(user)


# Login

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to listing page if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('listing'))
    form = LoginForm()
    users = mongo.db.users
    if form.validate_on_submit():
        user = users.find_one({'email' : form.email.data})
        # If user exists and password matches password in db, log in and create a user session
        if user and bcrypt.check_password_hash(user['password'], form.password.data.encode('utf-8')):
            username = user['username']
            login_user(User(user), remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome to squirrel, {username}.', 'success')

            # If unauthorized page has been accessed before being logged in,
            # redirect to it after login if it is safe
            if next_page and is_safe_url(next_page, socket.gethostname()):
                return redirect(next_page)

            # If not, redirect to the listing page
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
        # Create new user only if email is not already in use
        if existing_email is None:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            users.insert({
                "username": form.username.data,
                "email": form.email.data,
                "password": hashed_password,
            })
            # Log in once user is created in db
            user = users.find_one({'email': form.email.data})
            login_user(User(user), remember = False)
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


@app.route('/listing')
@app.route('/listing/<tag>')
@login_required
def listing(tag = None):
    # If a tag is passed as an argument, return a list of entries tagged as the argument
    if tag:
        entries = mongo.db.entries.find({'user_id' : current_user.id,  'tags': tag }).sort('_id', -1)
    # If no tags are passed as an argument, return a list of all entries
    else:
        entries = mongo.db.entries.find({'user_id' : current_user.id }).sort('_id', -1)
    return render_template('pages/listing.html',  title="Listing", entries=entries, tag=tag)


@app.route('/profile')
@login_required
def profile():
    return render_template('pages/profile.html',  title="Profile")


@app.route('/entry/<entry_id>')
@login_required
def entry(entry_id):
    form = EntryForm()
    the_entry = mongo.db.entries.find_one({"_id": ObjectId(entry_id)})
    form.name.data = the_entry["name"]
    form.description.data = the_entry["description"]
    form.rating.data = str(the_entry["rating"])
    form.hidden_tags.data = ','.join(the_entry["tags"])
    form.hidden_id.data = entry_id
    return render_template('pages/entry.html',  title="Entry" , entry=the_entry, form = form)


@app.route('/update_fav/<entry_id>', methods=['POST', 'GET'])
@login_required
def update_fav(entry_id):
    form = EntryForm()
    entries = mongo.db.entries
    timestamp = datetime.now()
    entries.update(
        {"_id": ObjectId(entry_id)},
        { "$set":
            {
                "is_fav": form.is_fav.data,
                "updated_on": timestamp
            }
        },
    )
    return jsonify( {"updated_on" : timestamp,
                    "success_message": "Review sucessfully updated.",
                    "message_class": "alert-success"})


@app.route('/update_name/<entry_id>', methods=['POST', 'GET'])
@login_required
def update_name(entry_id):
    form = EntryForm()
    entries = mongo.db.entries
    timestamp = datetime.now()
    entries.update(
        {"_id": ObjectId(entry_id)},
        { "$set":
            {
                "name": form.name.data,
                "updated_on": timestamp
            }
        },
    )
    return jsonify( {"updated_on" : timestamp,
                    "success_message": "Review sucessfully updated.",
                    "message_class": "alert-success"})


@app.route('/update_description/<entry_id>', methods=['POST', 'GET'])
@login_required
def update_description(entry_id):
    form = EntryForm()
    entries = mongo.db.entries
    timestamp = datetime.now()
    entries.update(
        {"_id": ObjectId(entry_id)},
        { "$set":
            {
                "description": form.description.data,
                "updated_on": timestamp
            }
        },
    )
    return jsonify( {"updated_on" : timestamp,
                    "success_message": "Review sucessfully updated.",
                    "message_class": "alert-success"})


@app.route('/update_rating/<entry_id>', methods=['POST', 'GET'])
@login_required
def update_rating(entry_id):
    form = EntryForm()
    entries = mongo.db.entries
    timestamp = datetime.now()
    entries.update(
        {"_id": ObjectId(entry_id)},
        { "$set":
            {
                "rating": int(form.rating.data),
                "updated_on": timestamp
            }
        },
    )
    return jsonify( {"updated_on" : timestamp,
                    "success_message": "Review sucessfully updated.",
                    "message_class": "alert-success"})



@app.route('/update_tags/<entry_id>', methods=['POST', 'GET'])
@login_required
def update_tags(entry_id):
    form = EntryForm()
    entries = mongo.db.entries
    timestamp = datetime.now()
    entries.update(
        {"_id": ObjectId(entry_id)},
        { "$set":
            {
                "tags": form.tags.data.split(","),
                "updated_on": timestamp
            }
        },
    )
    return jsonify( {"updated_on" : timestamp,
                    "success_message": "Review sucessfully updated.",
                    "message_class": "alert-success"})


@app.route('/update_image/<entry_id>', methods=['POST', 'GET'])
@login_required
def update_image(entry_id):
    form = EntryForm()
    entries = mongo.db.entries
    timestamp = datetime.now()
    image = request.files[form.image.name]
    uploaded_image = cloudinary.uploader.upload(image, width = 800, quality = 'auto')
    image_url = uploaded_image.get('secure_url')
    entries.update(
        {"_id": ObjectId(entry_id)},
        { "$set":
            {
                "image": image_url,
                "updated_on": timestamp
            }
        },
    )
    return jsonify({"new_image" : image_url,
                    "updated_on" : timestamp,
                    "success_message": image,
                    "message_class": "alert-success"})


@app.route('/add', methods=['GET', 'POST'])
@login_required
def new_entry():
    form = NewEntryForm()
    entries = mongo.db.entries
    if form.validate_on_submit():
        if form.image.data:
            image = request.files[form.image.name]
            uploaded_image = cloudinary.uploader.upload(image, width = 800, quality = 'auto')
            image_url = uploaded_image.get('secure_url')
        else:
            image_url = ''
        
        tags = form.tags.data.split(',')
        entries.insert({
            "name": form.name.data,
            "user_id": current_user.id,
            "description": form.description.data,
            "rating": int(form.rating.data),
            "is_fav": form.is_fav.data,
            "image" : image_url,
            "tags": tags,
            "created_on": datetime.now()
        })
        new_entry = mongo.db.entries.find_one({"name": form.name.data})
        new_entry_id = new_entry['_id']
        flash(f'Review for {form.name.data} created successfully.', 'success')
        return redirect(url_for('entry', entry_id = new_entry_id))
    return render_template('pages/new_entry.html',  title="New Entry", form=form)


@app.route('/delete/<entry_id>')
@login_required
def delete(entry_id):
    review_name = mongo.db.entries.find_one({"_id": ObjectId(entry_id)})["name"]
    mongo.db.entries.delete_one({"_id": ObjectId(entry_id)})
    flash(f'Review for {review_name} was deleted.', 'success')
    return redirect(url_for('listing'))



@app.route('/search')
@login_required
def search():
    return render_template('pages/search.html',  title="Search")


if __name__ == '__main__':
    app.run(host=os.environ.get('HOSTNAME'),
            port=int(os.environ.get('PORT')),
            debug=os.environ.get('DEV'))
