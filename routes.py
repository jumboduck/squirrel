from flask import render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, EntryForm,\
    NewEntryForm, UpdateAccount, SendFeedback
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from is_safe_url import is_safe_url
from datetime import datetime
from config import app, users, bcrypt, entries, text_regex, mail, playground_id
from update import update_field, update_success_msg, update_failure_msg
from login import User
from flask_mail import Message
import cloudinary
import cloudinary.uploader
import cloudinary.api
import math
import socket


"""
# About Route
# ===========
# The following route simply takes users to a page describing the application.
"""

@app.route('/about', methods=['GET'])
def about():
    return render_template('pages/about.html', title="About squirrel")

"""
# Login Route
# ===========
#
# The following manages the login route.
# If a session already exists, the user is redirected to the listing page.
#
# If not, the login page is displayed.
# Several requirements exist for the user to login upon submission
# of the form:
# 1) The account has to exist in the database
# 2) The submitted password has to match the hashed password saved in
# the database
#
# The 'next' argument is sent through the url if a user tried to access a
# page behinda login wall.
# This argument is used to redirect the user to the appropriate page,
# after having verified that it is a safe url.
"""


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to listing page if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('listing'))
    form = LoginForm()
    if form.validate_on_submit():
        user = users.find_one({'email': form.email.data})
        # If user exists and password matches password in db,
        # log in and create a user session
        if user and bcrypt.check_password_hash(
                        user['password'],
                        form.password.data.encode('utf-8')):
            username = user['username']
            # Save session, even after browser is closed
            login_user(User(user), remember=form.remember.data)

            # Checks where to redirect the user after login
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
            flash(
                'Login unsucessful, please check email and password.',
                'danger')

    return render_template('pages/login.html', title="Login", form=form)


"""
# Registration Route
# ==================
#
# The following manages new user registration.
# Upon form submission, if the email does not already exist as an account in
# the database, and the two password fields match, a new user is inserted.
# The password is hashed with bcrypt for added security.
#
# Once the account is created, the user is automatically logged in with this
# new account and redirected to the listing page.
"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('listing'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_email = users.find_one({'email': form.email.data})
        # Create new user only if email is not already in use
        if existing_email is None:
            hashed_password = bcrypt.generate_password_hash(
                                form.password.data
                                ).decode('utf-8')
            users.insert_one({
                "username": form.username.data,
                "email": form.email.data,
                "password": hashed_password,
            })
            # Log in once user is created in db
            user = users.find_one({'email': form.email.data})
            login_user(User(user), remember=False)
            flash(f'Account created for {form.username.data}.', 'success')
            return redirect(url_for('listing'))
        else:
            flash(f'Something went wrong with the information provided.',
                   'danger')

    return render_template(
                            'pages/registration.html',
                            title="Registration",
                            form=form)


"""
# Logout Route
# ============
#
# The following redirects the user to the login page and deletes the session
# cookie.
"""


@app.route('/logout')
def logout():
    logout_user()
    flash(f'Sucessfully logged out.', 'success')
    return redirect(url_for('login'))


"""
# Listing Route
# =============
#
# The following displays a listing of user reviews.
# The query to the database will be different if a tag has been passed to
# the url.
#
# Several variables are created to manage pagination:
# limit: defines the number of reviews to display on the page
# page: defines which page to be viewed, this is sent as an argument through
# the url
# offset: defines how many elements to skip in the database query
# max_page: defines the maximum number of pages
#
# If a non existant page is sent as an argument through the url, user is
# redirected to a 404 page.
#
# In the query to mongodb, a field called 'sort_date' is added to each result.
# It takes the value of 'updated_on' if existant, if not it takes the value of
# 'created_on'.
# This allows to sort the entries by their latest update or creation date.
"""


@app.route('/listing/')
@app.route('/listing/<tag>/')
@login_required
def listing(tag=None):

    # Change search query if tag exists or not
    if tag:
        match_query = {'user_id': current_user.id, 'tags': tag}
    else:
        match_query = {'user_id': current_user.id}

    # Number of entries per page
    limit = 12

    if 'page' in request.args and request.args['page'].isnumeric():
        # Define which page to view based on get request
        page = int(request.args['page'])
    else:
        # if no pages are defined, view page 1
        page = 1

    # Set index of first result of query
    offset = (page - 1) * limit

    # Count number of results for the query
    entry_count = entries.count_documents(match_query)
    max_page = math.ceil(entry_count/limit)

    # If a tag has been entered in the url but no entries are
    # tagged with the keyword, return a 404 error.
    if tag and entry_count == 0:
        return render_template('pages/404.html',  title="Page Not Found")

    # Ensure that if an inexistant page is entered in the address bar,
    # a 404 page is returned
    if entry_count != 0 and page > max_page or page <= 0:
        return render_template('pages/404.html',  title="Page Not Found")

    # Query that returns entries, sorted by creation date or update date
    entries_list = entries.aggregate([
        {'$match': match_query},
        {'$addFields': {
            # Sorts by created date, or updated date if it exists
            'sort_date': {
                '$cond': {
                    'if': '$updated_on',
                    'then': '$updated_on',
                    'else': '$created_on'
                }
            }
        }},
        {'$sort': {'sort_date': -1}},
        {'$skip': offset},
        {'$limit': limit}
    ])

    # Create next and previous urls for pagination
    current_url = request.path
    next_url = (current_url + "?page=" + str(page + 1)
                if (page + 1) <= max_page
                else None)
    prev_url = (current_url + "?page=" + str(page - 1)
                if (page - 1) > 0
                else None)

    return render_template(
        'pages/listing.html',
        title="Listing",
        entries=entries_list,
        tag=tag,
        next_url=next_url,
        prev_url=prev_url,
        entry_count=entry_count)


"""
# Entry Route
# ===========
# This route displays reviews generated by the user.
# If the entry was created by logged in user, it pulls its information
# from the database using its id.
#
# The input fields in the html are populated by this information from
# the database.
#
# If a user tries to access an entry created by another user (through the url),
# they are redirected to a 403 page.
"""


@app.route('/entry/<entry_id>/')
@login_required
def entry(entry_id):
    print(current_user.id)
    form = EntryForm()
    the_entry = entries.find_one({"_id": ObjectId(entry_id)})
    if the_entry["user_id"] == current_user.id:
        form.name.data = the_entry["name"]
        form.description.data = the_entry["description"]
        form.rating.data = str(the_entry["rating"])
        form.hidden_id.data = entry_id
        if the_entry.get("tags") is not None:
            form.hidden_tags.data = ','.join(the_entry["tags"])
        return render_template(
            'pages/entry.html',
            title="Entry",
            entry=the_entry,
            form=form)
    else:
        return render_template('pages/403.html',  title="Forbidden")


"""
# Update Routes
# =============
# The following routes are called with AJAX requests to make updates to the
# various fields of an entry without reloading the page.
# They return a JSON object to the page which is processed with JavaScript.
#
# These function each update the appropriate field in the database and updates
# the updated_on field with a new timestamp.
#
# On each of these routes, if the user tries to update an entry connected to
# another account, it returns a 403 error.
"""


# This route updates the is_fav status of the entry.
@app.route('/update_fav/<entry_id>', methods=['POST', 'GET'])
def update_fav(entry_id):
    the_entry = entries.find_one({"_id": ObjectId(entry_id)})
    form = EntryForm()
    timestamp = datetime.now()
    if the_entry["user_id"] == playground_id or the_entry["user_id"] == current_user.id:
        update_field(
            {"is_fav": form.is_fav.data,
             "updated_on": timestamp},
            entry_id)
        return update_success_msg("is_fav", timestamp)
    else:
        return render_template('pages/403.html',  title="Forbidden")


# This route updates the name of the entry.
# The database is only is updated if the submitted string is between 0 and 30
# characters long.
@app.route('/update_name/<entry_id>', methods=['POST', 'GET'])
def update_name(entry_id):
    form = EntryForm()
    new_name = form.name.data
    the_entry = entries.find_one({"_id": ObjectId(entry_id)})
    timestamp = datetime.now()
    if the_entry["user_id"] == playground_id or the_entry["user_id"] == current_user.id:
        if (len(new_name) > 0 and
                len(new_name) <= 30 and
                text_regex.match(new_name)):
            update_field(
                {"name": form.name.data,
                 "updated_on": timestamp},
                entry_id)
            return update_success_msg("Name", timestamp)
        else:
            return update_failure_msg("Name must be betwen 1 and 30 "
                                      "characters, and cannot start with"
                                      " a space.")
    else:
        return render_template('pages/403.html',  title="Forbidden")


# This route updates the description of the entry.
# The database is only is updated if the submitted string is between 0 and 2000
# characters long.
@app.route('/update_description/<entry_id>', methods=['POST', 'GET'])
def update_description(entry_id):
    timestamp = datetime.now()
    form = EntryForm()
    new_description = form.description.data
    the_entry = entries.find_one({"_id": ObjectId(entry_id)})
    if the_entry["user_id"] == playground_id or the_entry["user_id"] == current_user.id:
        if (len(new_description) > 0 and
                len(new_description) <= 2000 and
                text_regex.match(new_description)):
            update_field(
                {"description": form.description.data,
                 "updated_on": timestamp},
                entry_id)
            return update_success_msg("Description", timestamp)
        else:
            return update_failure_msg("Description must be betwen 1 and 2000 "
                                      "characters, and cannot start with a "
                                      "space or line break.")
    else:
        return render_template('pages/403.html',  title="Forbidden")


# This route updates the rating of the entry.
# It ensures that the data sent to the database is an integer,
# and not a string.
@app.route('/update_rating/<entry_id>', methods=['POST', 'GET'])
def update_rating(entry_id):
    timestamp = datetime.now()
    form = EntryForm()
    the_entry = entries.find_one({"_id": ObjectId(entry_id)})
    if the_entry["user_id"] == playground_id or the_entry["user_id"] == current_user.id:
        update_field(
            {"rating": int(form.rating.data),
             "updated_on": timestamp},
            entry_id)
        return update_success_msg("Rating", timestamp)
    else:
        return render_template('pages/403.html',  title="Forbidden")


# This route updates the tags of the entry.
@app.route('/update_tags/<entry_id>', methods=['POST', 'GET'])
def update_tags(entry_id):
    timestamp = datetime.now()
    form = EntryForm()
    the_entry = entries.find_one({"_id": ObjectId(entry_id)})
    if the_entry["user_id"] == playground_id or the_entry["user_id"] == current_user.id:
        # If the tag list sent to python is empty, remove field from db
        if len(form.tags.data) == 0:
            entries.update_one(
                                {"_id": ObjectId(entry_id)},
                                {"$unset":
                                    {
                                        "tags": "",
                                        "updated_on": timestamp
                                    }
                                 }
                             )
            return update_success_msg("Tags", timestamp)

        else:
            # If there is a list of tags, turn tags to a lowercase list and
            # remove any duplicates
            lowercase_tags = form.tags.data.lower().split(',')

            final_tags = []
            for tag in lowercase_tags:
                if tag not in final_tags:
                    final_tags.append(tag)
            update_field(
                {"tags": final_tags,
                 "updated_on": timestamp},
                entry_id)
            return update_success_msg("Tags", timestamp)
    else:
        return render_template('pages/403.html',  title="Forbidden")


# This route updates the image of the entry.
# It retrieves the new image's url and its public id from cloudinary to store
# in the database.
@app.route('/update_image/<entry_id>', methods=['POST', 'GET'])
def update_image(entry_id):
    timestamp = datetime.now()
    form = EntryForm()
    image = request.files[form.image.name]
    # The new image is uploaded to cloudinary and its url and id are retrieved
    uploaded_image = cloudinary.uploader.upload(
                                                image, width=800,
                                                quality='auto'
                                                )
    image_url = uploaded_image.get('secure_url')
    new_image_id = uploaded_image.get('public_id')
    the_entry = entries.find_one({"_id": ObjectId(entry_id)})
    # The previous image in is deleted from cloudinary to not crowd it with
    # unused images
    cloudinary.uploader.destroy(the_entry["image_id"])
    # Image fields are updated in the database
    if the_entry["user_id"] == playground_id or the_entry["user_id"] == current_user.id:
        update_field(
            {"image": image_url,
             "image_id": new_image_id,
             "updated_on": timestamp},
            entry_id)

        return update_success_msg("Image", timestamp, image_url)
    else:
        return render_template('pages/403.html',  title="Forbidden")

"""
# Add Route:
# ==========
#
# This route allows users to add a new entry to the database.
# Upon validation, every field is checked and inserted into mongodb as a new
# document.
"""


@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_entry():
    form = NewEntryForm()
    if form.validate_on_submit():
        # Images are uploaded to cloudinary, and their url
        # is inserted into the image field of the database.
        if form.image.data:
            image = request.files[form.image.name]
            uploaded_image = cloudinary.uploader.upload(
                image,
                width=800,
                quality='auto'
            )
            image_url = uploaded_image.get('secure_url')
            image_id = uploaded_image.get('public_id')

        else:
            # A default placeholder image is selected
            # if no image has been inputed.
            image_url = '/static/img/image-placeholder.png'
            image_id = 'blank'

        # The tags are retrieved as a string of words separated by commas.
        # We generate a list by splitting the string, words are lowercased
        # and we ensure no tags are duplicated.
        if form.hidden_tags.data != "":
            lowercase_tags = form.hidden_tags.data.lower().split(',')
            tags = []
            for tag in lowercase_tags:
                if tag not in tags:
                    tags.append(tag)

        else:
            tags = None

        # The data from the form creates a new document in the database.
        new_entry_id = entries.insert_one({
            "name": form.name.data,
            "user_id": current_user.id,
            "description": form.description.data,
            "rating": int(form.rating.data),
            "is_fav": form.is_fav.data,
            "image": image_url,
            "image_id": image_id,
            "tags": tags,
            "created_on": datetime.now()
        })

        flash(
            f'Review for “{form.name.data}” created successfully.',
            'success'
        )

        return redirect(url_for('entry', entry_id=new_entry_id.inserted_id))
    else:
        # If form does not validate, empty the hidden tags field
        form.hidden_tags.data = ""

    return render_template(
        'pages/new_entry.html',
        title="New Entry",
        form=form
    )


"""
# Delete Entry Route
# ==================
#
# The following checks that the current user created the entry
# and removes the document from the database.
# If a different user created the document, they are redirected to
# a 403 error.
"""


@app.route('/delete/<entry_id>/')
@login_required
def delete(entry_id):
    the_entry = entries.find_one({"_id": ObjectId(entry_id)})
    if the_entry["user_id"] == current_user.id:
        review_name = the_entry["name"]
        image_id = the_entry["image_id"]
        entries.delete_one({"_id": ObjectId(entry_id)})
        cloudinary.uploader.destroy(image_id)
        flash(f'Review for “{review_name}” was deleted.', 'success')
        return redirect(url_for('listing'))
    else:
        return render_template('pages/403.html',  title="Forbidden")


"""
# Profile Route
# =============
#
# This route displays the user profile, which contains statistics about
# their squirrel repository, such as number of reviews, number of favorites,
# average rating, most used tags.
# It also allows for users to update their username, password, and email
# address.
"""


@app.route('/profile/', methods=["POST", "GET"])
@login_required
def profile():
    form = UpdateAccount()
    # Count the number of entries created by user
    num_entries = entries.count_documents({'user_id': current_user.id})
    # Count the number of entries favorites by user
    num_fav = entries.count({'user_id': current_user.id, 'is_fav': True})
    # Find average rating of all reviews created by user
    avg_rating = entries.aggregate([
        {"$match": {"user_id": current_user.id}},
        {"$group": {
                "_id": None,
                "result": {"$avg": "$rating"}
           }
         }
    ])

    # The average is rounded to the second decimal.
    # If no entries have been created, the average sent to the html
    # template is 0.
    if num_entries == 0:
        rounded_avg = 0
    else:
        rounded_avg = round(list(avg_rating)[0]['result'], 2)

    # The following manages updates of the account information.
    # Data from each field is sent to update the user document in mongodb.
    # If a field is left blank, the current user's data for that field is
    # sent instead.
    if form.is_submitted():
        if form.validate() and bcrypt.check_password_hash(
                                current_user.password,
                                form.password.data.encode('utf-8')):

            if form.username.data:
                new_username = form.username.data
            else:
                new_username = current_user.username

            if form.email.data:
                new_email = form.email.data
            else:
                new_email = current_user.email

            if form.new_password.data:
                new_password = bcrypt.generate_password_hash(
                                        form.new_password.data
                                        ).decode('utf-8')
            else:
                new_password = current_user.password

            users.update_one(
                {"_id": current_user.id},
                {"$set":
                    {
                        "username": new_username,
                        "email": new_email,
                        "password": new_password
                    }
                 }
            )
            flash("Account information updated successfully", "success")
            # A redirect is used to reload the page, to ensure that the newly
            # updated information is displayed
            return redirect(url_for("profile"))

        else:
            flash("There was a problem updating your information.", "danger")
    return render_template(
        'pages/profile.html',
        title="Profile",
        num_entries=num_entries,
        num_fav=num_fav,
        avg_rating=rounded_avg,
        username=current_user.username,
        email=current_user.email,
        form=form
    )


"""
# Search Routes
# =============
#
# This first route sends the information from the search bar to
# the search results route.
"""


@app.route('/search/', methods=["POST"])
@login_required
def get_search():
    return redirect(url_for(
        "search",
        search_term=request.form.get("search_field")
    ))


"""
# This route generates the search results.
"""


@app.route('/search/<search_term>/', methods=["POST", "GET"])
@login_required
def search(search_term):
    entries.create_index([
        ("name", "text"),
        ("description", "text"),
        ("tags", "text"),
    ])

    result = entries.find(
        {
            'user_id': current_user.id,
            "$text": {"$search": search_term}
        },
        {
            'score': {'$meta': 'textScore'}
        }).sort(
            [('score', {'$meta': 'textScore'})]
        )

    # Count the number of results of the query
    num_entries = len(list(result.clone()))

    return render_template(
        'pages/search.html',
        title="Results for " + search_term,
        num_entries=num_entries,
        entries=result,
        search_term=search_term
    )


"""
# Feedback Route
# ==============
# This route displays the feedback form for users to report bugs
# or other feedback.
"""

@app.route('/feedback/', methods=['GET', 'POST'])
@login_required
def feedback():
    form = SendFeedback()
    if form.validate_on_submit():
        msg = Message(subject=f"Squirrel Feedback from {current_user.username}",
                      body=f"Feedback from: {current_user.username } at {current_user.email}\n{form.message.data}",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[app.config.get("MAIL_USERNAME")])
        mail.send(msg)
        flash("Thank you for your feedback!", "success")
        return redirect(url_for('listing'))
    return render_template('pages/feedback.html',
                           form=form,
                           title="Feedback")


# This route handles 404 errors
@app.errorhandler(404)
def invalid_route(e):
    return render_template('pages/404.html',  title="Page Not Found")
