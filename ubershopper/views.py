# -*- coding: utf-8 -*-
# Views modules.  Controller which handle the request-response-flow.  They typically call services to provide
# data and perform actions.  They should not communicate directly with models and providers.
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from ubershopper import app, db, tools, models, auth
import json
from bson import json_util


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.route('/accounts/api/v1.0/users', methods=['GET'])
@auth.login_required
def get_tasks():
    users = db.users
    data = [user.as_dict() for user in users.User.find()]
    return tools.mongodoc_jsonify({'users': data})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(expiration=600)
    return jsonify({'token': token.decode('ascii')})

@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    users = db.users
    if users.User.find_one({'username': username}) is not None:
        abort(400)  # existing user
    user = users.User()
    user.username = username
    user.set_password(password)
    user.save()
    return jsonify({'username': user.username}), 201, {'Location': url_for('get_tasks')}
