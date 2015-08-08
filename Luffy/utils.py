# -*- coding:utf-8 -*-

import urlparse
import pymongo

from .settings import MONGO_URI, MONGO_DATABASE

db = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE]


def leaf():
    return [x['path'] for x in db['books'].find({'download': False}, projection={'_id': False, 'path': True})]
