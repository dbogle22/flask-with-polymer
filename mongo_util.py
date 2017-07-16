from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
import re
# import requests

# FIXME: Make sure this is correct
log = logging.Logger(__name__)
log.setLevel(logging.INFO)
TOTAL_RUNNING = 26.2
TOTAL_BIKING = 112.0
TOTAL_SWIMMING = 2.4

class mongo(object):
    """
    This class is used a context manager for a mongo database instance
    It ensures that the db object gets properly closed after each time
    it is used
    """
    def __init__(self, url='mongodb://localhost:27017/', db_name='iron'):
        self.url = url

    def __enter__(self):
        self.client = MongoClient(self.url, connect=True, socketTimeoutMS=5000, connectTimeoutMS=5000, serverSelectionTimeoutMS=5000)
        self.db_conn = self.client.iron
        return self.db_conn

    def __exit__(self, *args):
        self.client.close()

def get_user(user):
    with mongo() as db:
        log.info('Searching for user "%s"' % user.username)
        print('Searching for user "%s"' % user.username)
        return db.users.find_one({'username': user.username})


def get_leaderboard():
    with mongo() as db:
        return db.users.find({})

def update_user_stats(user, **kwargs):
    with mongo() as db:
        print(kwargs)
        found_user = db.users.find_one({'username': user.username})
        new_running = float(kwargs.get('running', 0)) + float(found_user['running'])
        new_biking = float(kwargs.get('biking', 0)) + float(found_user['biking'])
        new_swimming = float(kwargs.get('swimming', 0)) + float(found_user['swimming'])

        if new_running > TOTAL_RUNNING:
            raise Exception("New running amount exceeds the total miles needed")
        if new_biking > TOTAL_BIKING:
            raise Exception("New biking amount exceeds the total miles needed")
        if new_swimming > TOTAL_SWIMMING:
            raise Exception("New swimming amount exceeds the total miles needed")

        new_percent_complete = ((new_running / TOTAL_RUNNING) * 100
                               + (new_biking / TOTAL_BIKING) * 100
                               + (new_swimming / TOTAL_SWIMMING) * 100) / 3
        result = db.users.update_one({'username': user.username}, {'$set':
                                                                   {
                                                                    'running': new_running,
                                                                    'biking': new_biking,
                                                                    'swimming': new_swimming,
                                                                    'percent_complete': new_percent_complete
                                                                   }
                                                                 }
                            )

def check_if_user_exists(userName):
    with mongo() as db:
        regx_search = re.compile('^' + userName + '$', re.IGNORECASE)
        if db.users.find({'username': regx_search}).count() == 0:
            return False
        else:
            return True
