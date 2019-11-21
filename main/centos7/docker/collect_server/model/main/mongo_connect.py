#!/usr/bin/env python
# coding:utf-8

import pymongo
import gridfs
import datetime

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from env import settings

# DBのホスト/ポートの設定
host = settings.DB_HOST
port = settings.DB_PORT

# ユーザ/パスワード
user = settings.DB_USER
pwd = settings.DB_PASS

#  DBの名前/コレクションの設定
db_name = settings.DB_NAME
db_col = settings.DB_COL


class Students_DB:
    def __init__(self, *args, **kwargs):
        self.client = pymongo.MongoClient(host, port)
        self.client[db_name].authenticate(user, pwd)

    def insert(self, collection, dict={}):
        self.col = self.client[db_name][collection]
        return self.col.insert(dict)

    def find(self, collection, dict={}):
        self.col = self.client[db_name][collection]
        return self.col.find(dict)

    def distinct(self, collection, feild):
        self.col = self.client[db_name][collection]
        return self.col.distinct(feild)
