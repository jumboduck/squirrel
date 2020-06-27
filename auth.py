from app import mongo, login_manager
from bson.objectid import ObjectId
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, username, id):
     self.id = id
     self.email = email
     self.username = username

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


@login_manager.user_loader
def load_user(user_id):
    user =  mongo.db.users.find_one({'_id' : ObjectId(user_id)})
    return User(user.email, user.username, ObjectId(user._id))