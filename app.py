import bson.json_util
import mongo_util
import os
import logging
from models import User
from pymongo import MongoClient
from flask import Flask, request, redirect, url_for, abort
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
app.logger.setLevel(logging.INFO)

@login_manager.user_loader
def user_loader(user_id):
    with mongo_util.mongo() as db:
        app.logger.info('User id: %s' % user_id)

        user = db.users.find_one({'username': user_id})
        app.logger.info(user)

        new_user = User(user['username'], user['password'])
        app.logger.info(new_user)
        return new_user

@app.route('/')
@login_required
def hello():
    return app.send_static_file('index.html')

@app.route('/getUserStats')
def get_user_stats():
    logged_in_user = mongo_util.get_user(current_user)
    app.logger.info(logged_in_user)
    if logged_in_user:
        return bson.json_util.dumps(logged_in_user)
    else:
        return bson.json_util.dumps({'error': 'Could not find logged in user'}), 500

@app.route('/updateUserStats')
@login_required
def update_user_stats():
    run = request.args.get('running', 0.0)
    bike = request.args.get('biking', 0.0)
    swim = request.args.get('swimming', 0.0)
    try:
        result = mongo_util.update_user_stats(current_user, running=run, biking=bike, swimming=swim)
        app.logger.info(result)
        return bson.json_util.dumps({'result': True})
    except Exception as e:
        return bson.json_util.dumps({'error': str(e)}), 400

@app.route('/getLeaderBoard')
def get_leader_board():
    leader = list(mongo_util.get_leaderboard())
    for i in leader:
        del i['password']
        del i['_id']
    return bson.json_util.dumps(sorted(leader, key=lambda k: k['percent_complete'], reverse=True))

@app.route('/doLogin', methods=['GET', 'POST'])
def do_login():
    # if request.method == 'POST':
    #     with mongo_util.mongo() as db:
    #         body = request.get_json()
    #         app.logger.debug(body)
    #         body['password'] = generate_password_hash(body['password'])
    #
    #         # Make sure this actually worked
    #         if not mongo_util.check_if_user_exists(body['userName']):
    #             user = db.users.insert_one(body)
    #             app.logger.debug(user.inserted_id)
    #             if user.inserted_id:
    #                 # Add User to database
    #                 new_user = User(body['firstName'], body['lastName'], body['userName'], body['email'], body['password'])
    #                 new_user.authenticated = True
    #                 login_user(new_user)
    #                 return redirect('/profile')
    #         else:
    #             return bson.json_util.dumps({'status': 500, 'response': 'Failed to add new user'}), 500
    if request.method == 'GET':
        with mongo_util.mongo() as db:
            username = request.args.get('username', '')
            password = request.args.get('password', '')

            if username == '' or password == '':
                return bson.json_util.dumps({'status': 200, 'response': 'Bad request'})

            # Verify credentials
            user = db.users.find_one({'username': username})
            app.logger.info(user)
            if user:
                # User already exists so log them in
                new_user = User(user['username'], user['password'])
                if check_password_hash(user['password'], password):
                    app.logger.info("New user: %s" % str(new_user))
                    if not login_user(new_user):
                        return bson.json_util.dumps({'status': 200, 'response': 'Login failed'}), 200
                    app.logger.info("New user: %s" % str(new_user))
                    return bson.json_util.dumps({'status': 200, 'response': 'Successfully logged in'}), 200
                else:
                    return bson.json_util.dumps({'status': 200, 'response': 'Incorrect username or password'}), 200
            else:
                # A new user should be created
                password = generate_password_hash(password)
                user = db.users.insert_one({'username': username, 'password': password, 'running': 0.0, 'biking': 0.0, 'swimming': 0.0, 'percent_complete': 0.0})
                app.logger.info(dir(user))
                if user.inserted_id:
                    new_user = User(username, password)
                    new_user.authenticated = True
                    login_user(new_user)
                    app.logger.info('Changing to profile page')
                    return redirect('/view1')


@app.route('/<path:the_path>')
def all_other_routes(the_path):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
