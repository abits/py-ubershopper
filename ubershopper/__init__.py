# -*- coding: utf-8 -*-
from flask import Flask, g
from flask.ext.mongokit import Connection
from flask.ext.login import LoginManager
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_pyfile('../config.py')
connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])
db = connection[app.config['MONGODB_NAME']]
auth = HTTPBasicAuth()

from ubershopper import views, models
connection.register([models.User])


@auth.verify_password
def verify_password(username_or_token, password):
    users = db.users
    user = models.User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = users.User.one({'username': username_or_token})
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True
