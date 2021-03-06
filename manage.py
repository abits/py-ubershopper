# -*- coding: utf-8 -*-
#!venv/bin/python
from flask.ext.script import Manager
from ubershopper import app, db, fixtures as Fixtures
from flask_debugtoolbar import DebugToolbarExtension


manager = Manager(app)

@manager.command
def runserver():
    app.config['DEBUG'] = True
    toolbar = DebugToolbarExtension(app)
    app.run(host='127.0.0.1',
            port=5000)

@manager.command
def fixtures():
    Fixtures.load(db)


if __name__ == "__main__":
    manager.run()
