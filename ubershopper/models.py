# -*- coding: utf-8 -*-
# Models module.  This module contains model classes which abstract the persistence layer.
# It may also define transient data structures which hold generated data the services layer has to deal with.

import tools
from bson import ObjectId
from flask import g
from flask.ext.mongokit import Document
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from ubershopper import app, auth, db

class User(Document):
    structure = {
        'username': unicode,
        'firstname': unicode,
        'lastname': unicode,
        'email': unicode,
        'pw_hash': basestring,
        'last_login': {
            'date': datetime,
            'ip': basestring
        },
        'created_at': datetime,
        'modified_at': datetime,
        'deleted_at': datetime,
    }
    validators = {
        'username': tools.max_length(50),
        'email': tools.max_length(120)
    }

    use_dot_notation = True
    use_autorefs = True

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def __repr__(self):
        return '<User: %r>' % self.username

    def as_dict(self):
        return {
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'last_login': {
                'date': self.last_login['date'],
                'ip': self.last_login['ip']
            },
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'deleted_at': self.deleted_at,
        }

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': str(self._id)})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        users = db.users
        user = users.User.find_one({'_id': ObjectId(data['id'])})
        g.user = user
        return user
