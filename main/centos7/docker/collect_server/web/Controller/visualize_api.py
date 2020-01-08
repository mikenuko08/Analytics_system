# coding: utf-8
import os
import re
from pymongo import MongoClient
import gridfs
import sys
import datetime
import json
import math
from bson.json_util import loads
from flask import Flask, abort, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

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

#  DB名
db_name = 'students'

# コレクション
st = 'status'
an = 'status_analysis'

client = MongoClient(db_url)
st_col = client[db_name][st]
an_col = client[db_name][an]

app = Flask(__name__)
api = Api(app)
CORS(app)


class ServerStatusList(Resource):
    def get(self):
        group = st_col.distinct('group')
        collection_time = st_col.distinct('collection_time')
        steps = st_col.distinct('step')
        status = {'group': group,
                  'collection_time': collection_time, 'steps': steps}
        return status

    def post(self):
        json_data = request.get_json()
        group = json_data['group']
        collection_time = json_data['collection_time']
        step = json_data['step']
        # print("group: ", end="")
        # print(group)
        # print("collection_time: ", end="")
        # print(collection_time)
        # print("step: ", end="")
        # print(step)

        dist = {"collection_time": collection_time, "step": step}
        display = {'_id': 0, 'collection_time': 0, 'step': 0}
        analysis = list(an_col.find(dist, display))[0]
        # amini = analysis['avarage_min_index']

        dist2 = {"group": group, "collection_time": collection_time, "step": step}
        display2 = {'_id': 0, 'group': 0, 'step': 0}
        data = [[], []]

        for doc in st_col.find(dist2, display2):
            if type(doc['stdout']) != str:
                doc['stdout'] = 'N/A'
            if type(doc['stderr']) != str:
                doc['stderr'] = 'N/A'
            data[0].append({'id': doc['id'], 'host': doc['host'], 'collection_time': doc['collection_time'], 'command': doc['command'],
                            'stdout': doc['stdout'], 'stderr': doc['stderr'], 'detail_collection_time': doc['detail_collection_time']})

        data[1].append(analysis)
        # print(rows)
        # print(type(testdata))
        return data


class ServerCommandList(Resource):
    pass


class ServerFileList(Resource):
    pass


api.add_resource(ServerStatusList, '/api/server_status')
api.add_resource(ServerCommandList, '/api/server_command')
api.add_resource(ServerFileList, '/api/server_File')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
