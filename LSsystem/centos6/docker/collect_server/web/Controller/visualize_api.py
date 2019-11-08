# coding: utf-8
import os
import re
import pymongo
import gridfs
import sys
import datetime
import json
import math
from bson.json_util import loads
from flask import Flask, abort, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

# dbの設定
host = "150.89.223.120"
port = 27017
db_name = 'students'

# ユーザ/パスワード
user = 'student'
pwd = 'student'

# コレクション
st = 'status'
an = 'analysis'

# DBに接続
client = pymongo.MongoClient(host, port)
client[db_name].authenticate(user, pwd)
st_col = client[db_name][st]
an_col = client[db_name][an]

app = Flask(__name__)
api = Api(app)
CORS(app)


class CreateUsersList(Resource):
    def get(self):
        pass

    def post(self):
        pass


class ServerStatusCommandList(Resource):
    def get(self):
        pass

    def post(self):
        pass


class ServerStatusList(Resource):
    def get(self):
        group = st_col.distinct('group')
        unixtimes = st_col.distinct('unixtime')
        steps = st_col.distinct('step')
        status = {'group': group, 'unixtimes': unixtimes, 'steps': steps}
        return status

    def post(self):
        json_data = request.get_json()
        group = json_data['group']
        unixtime = json_data['unixtime']
        step = json_data['step']
        dist = {"group": group, "unixtime": unixtime, "step": step}
        display = {'_id': 0, 'group': 0, 'step': 0}
        data = []
        for doc in st_col.find(dist, display):
            if type(doc['stdout']) != str:
                doc['stdout'] = 'N/A'
            if type(doc['stderr']) != str:
                doc['stderr'] = 'N/A'
            data.append({'id': doc['id'], 'host': doc['host'], 'unixtime': doc['unixtime'],
                         'command': doc['command'], 'stdout': doc['stdout'], 'stderr': doc['stderr'], 'date': doc['date']})
        # print(rows)
        # print(type(testdata))
        return data


api.add_resource(CreateUsersList, '/api/users')
api.add_resource(ServerStatusCommandList, '/api/server_status_command')
api.add_resource(ServerStatusList, '/api/server_status')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
