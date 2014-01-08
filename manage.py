# -*- coding: utf-8 -*-
#!venv/bin/python
from flask.ext.script import Manager
from ubershopper import app
from flask_debugtoolbar import DebugToolbarExtension


manager = Manager(app)

@manager.command
def hello():
    print "hello"

@manager.command
def runserver():
    app.config['DEBUG'] = True
    toolbar = DebugToolbarExtension(app)
    app.run(host='127.0.0.1',
            port=5000)

if __name__ == "__main__":
    manager.run()