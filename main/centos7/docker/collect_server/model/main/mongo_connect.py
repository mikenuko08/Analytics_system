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

    def find(self, dict={}, limit=0, descending=False, field='', count=False):
        self.database = self.client[self.db][self.col]
        if limit >= 1 and descending and count:
            result = self.database.find(dict).sort(
                field, -1).limit(limit)
            return result.count(True)

        if limit >= 1 and descending:
            result = self.database.find(dict).sort(
                field, -1).limit(limit)
            return result
        elif limit >= 1 and count:
            result = self.database.find(dict).limit(limit)
            return result.count(True)
        elif descending and count:
            result = self.database.find(dict).sort(
                field, -1)
            return result.count(True) 
        elif limit >= 1:
            return self.database.find(dict).limit(limit)
        elif descending:
            result = self.database.find(dict).sort(
                field, -1)
            return result
        elif count:
            result = self.database.find(dict)
            return result.count(True)
        return self.database.find(dict)

    def distinct(self, field):
        self.database = self.client[self.db][self.col]
        # if descending:
        #     result = self.database.distinct(field).sort(
        #         field, -1)
        #     return result
        return self.database.distinct(field)


# if __name__ == "__main__":
    # dic = {"name": "kanou"}
    # st = DBController("students", "status")
    # st.insert(dic)
    # # for s in st.find({'name': 'sato'}, 1, True, '_id'):
    # #     print(s)
    # print(st.distinct("name"))
