import datetime
import mongo_util
from bson import ObjectId
from flask_login import UserMixin

class User(UserMixin):
    _id = ObjectId()
    username = ""
    password = ""
    sign_up_date = ""
    last_login = ""

    def __init__(self,username, password):
        self.username = username
        self.password = password
        self.running = 0.0
        self.biking = 0.0
        self.swimming = 0.0
        self.percent_complete = 0.0
        self.sign_up_date = datetime.datetime.today().strftime("%B %d, %Y")
        self.last_login = datetime.datetime.today().strftime("%B %d, %Y")

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        result = "="*15 + "\n"
        result += "Username: %s\n" % self.username
        result += "Running: %d\n" % self.running
        result += "Biking: %d\n" % self.biking
        result += "Swimming: %d" % self.swimming
        result += "Sign up date: %s\n" % self.sign_up_date
        result += "Last login: %s\n" % self.last_login
        result += "Anonymous: %s\n" % self.is_anonymous
        result += "Authenticated: %s\n" % self.is_authenticated
        result += "Active: %s\n" % self.is_active
        result += "="*15 + "\n"
        return result

    def get_id(self):
        return self.username
