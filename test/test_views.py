# -*- coding: utf-8 -*-
#!venv/bin/python
import unittest
from multiprocessing import Process
import requests
import json
import sys, os
sys.path.append(os.path.abspath(os.getcwd()))
from ubershopper import app


def run_server():
    app.config['DEBUG'] = False
    app.run(host='127.0.0.1',
            port=5000)


class ListUsersTestCase(unittest.TestCase):
    def setUp(self):
        self.server = Process(target=app.run)
        self.server.start()
        r = requests.get('http://127.0.0.1:5000/api/token', auth=('admin', 'password'))
        body = json.loads(r.text)
        r = requests.get('http://127.0.0.1:5000/api/users', auth=(str(body['token']), 'test'))
        self.body = json.loads(r.text)
        self.headers = json.loads(r.headers)
        print self.body

    def tearDown(self):
        self.server.terminate()
        self.server.join()

    def test_mimetype(self):
        expected = 'application/vnd.collection+json'
        self.assertEqual(self.headers['content-type'], expected)

    def test_syntax(self):
        print self.body
        pass

if __name__ == '__main__':
    unittest.main()

