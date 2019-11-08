#!/usr/bin/env python
# coding:utf-8

import pymongo
import gridfs
import sys
import datetime

#dbの設定
host = "150.89.223.120"
port = 27017
db_name = 'students'

#ユーザ/パスワード
user = 'student'
pwd = 'student'

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
