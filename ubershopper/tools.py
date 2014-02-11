# -*- coding: utf-8 -*-
# Tools module.
# This module contains static helper functions.  They should receive all dependencies as parameters.
# You should not need classes in here. If you feel the need, consider adding a service class.
from datetime import datetime
from bson import ObjectId
import simplejson
from flask import Response


def max_length(length):
    """Check for max length of string."""
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)
    return validate


class MongoDocumentEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, ObjectId):
            return str(o)
        return simplejson.JSONEncoder(self, o)


def mongodoc_jsonify(*args, **kwargs):
    return Response(simplejson.dumps(dict(*args, **kwargs), cls=MongoDocumentEncoder), mimetype='application/json')


def collectify(**kwargs):
    collection = {
        'collection': {
            'version': kwargs['version'],
            'href': kwargs['href'],
            'items': kwargs['items']
        }
    }
    return Response(simplejson.dumps(collection, cls=MongoDocumentEncoder),
                    mimetype='application/vnd.collection+json')
