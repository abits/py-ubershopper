# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongokit import Connection
from models import User
from datetime import datetime


def load(db):
    create_admin_user(db)


def create_admin_user(db):
    users = db.users
    if not users.one({'username': u'admin'}):
        admin = users.User()
        admin.username = u'admin'
        admin.email = u'ubershopper@localhost'
        admin.credentials = {}
        admin.firstname = u'Admin'
        admin.lastname = u'Admin'
        admin.created_at = datetime.utcnow()
        admin.modified_at = datetime.utcnow()
        admin.deleted_at = None
        admin.set_password('password')
        admin.save()

if __name__ == '__main__':
    load()