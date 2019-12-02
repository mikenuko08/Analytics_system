#!/usr/bin/env python
# coding:utf-8

from pymongo import MongoClient
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
pawd = settings.DB_PASS

# DBのURL
db_url = "mongodb://" + user + ":" + pawd + "@" + host + ":" + port


class DBController:
    def __init__(self, db_name, collection, *args, **kwargs):
        self.client = MongoClient(db_url)
        self.db = db_name
        self.col = collection

    def insert(self, dict={}):
        self.database = self.client[self.db][self.col]
        return self.database.insert(dict)

    def find(self, dict={}, limit=0, count=False):
        self.database = self.client[self.db][self.col]
        if count and limit >= 1:
            result = self.database.find(dict).limit(limit)
            return result.count(True)
        elif count:
            result = self.database.find(dict)
            return result.count(True)
        elif limit >= 1:
            return self.database.find(dict).limit(limit)
        return self.database.find(dict)

    def distinct(self, feild):
        self.database = self.client[self.db][self.col]
        return self.database.distinct(feild)


# if __name__ == "__main__":
#     dic = {"name": "sato"}
#     st = DBController("students", "status")
#     st.insert(dic)
#     print(len(list(st.find())))
#     print(st.distinct("name"))
