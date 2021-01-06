from flask import render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, EntryForm,\
    NewEntryForm, UpdateAccount, SendFeedback
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from is_safe_url import is_safe_url
from datetime import datetime
from config import app, users, bcrypt, entries, text_regex, mail
from update import update_field, update_success_msg, update_failure_msg
from login import User
from flask_mail import Message
import cloudinary
import cloudinary.uploader
import cloudinary.api
import math
import socket

@app.route('/playground/')
@app.route('/playground/<tag>/')
def playground(tag=None):

    # Change search query if tag exists or not
    if tag:
        match_query = {'user_id': ObjectId('5f81b103c984b7e86dc415ad'), 'tags': tag}
    else:
        match_query = {'user_id': ObjectId('5f81b103c984b7e86dc415ad')}


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
    ])

    return render_template(
        'pages/listing.html',
        title="Listing",
        entries=entries_list,
        tag=tag,
        entry_count=1,
        playground=True)


@app.route('/playground/entry/<entry_id>/')
def playground_entry(entry_id):
    form = EntryForm()
    the_entry = entries.find_one({"_id": ObjectId(entry_id)})
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
        form=form,
        playground=True)

