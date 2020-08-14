
from flask_login import LoginManager, UserMixin
from config import app, users
from bson.objectid import ObjectId

"""
# USER MANAGEMENT
# ===============
# The following uses flask_login to create a user class that will be used
# throughout the application.
"""


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)



class User(UserMixin):
    def __init__(self, user):
        self.user = user
        self.username = user['username']
        self.id = user['_id']
        self.email = user['email']
        self.password = user['password']

    def get_id(self):
        object_id = self.user['_id']
        return str(object_id)


@login_manager.user_loader
def load_user(user_id):
    user = users.find_one({'_id': ObjectId(user_id)})
    return User(user)