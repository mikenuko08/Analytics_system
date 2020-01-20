# coding: utf-8
import os
import re
import sys
import datetime
import json
import math
from bson.json_util import loads

from pymongo import MongoClient
from flask import Flask, render_template, abort, request, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_cors import CORS

from datetime import datetime, time, timedelta, timezone
from dateutil.parser import parse
from collections import defaultdict
import re


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
ch = 'command_history'
cs = 'command_script'
fi = 'file_edit'

client = MongoClient(db_url)
st_col = client[db_name][st]
an_col = client[db_name][an]
ch_col = client[db_name][ch]
cs_col = client[db_name][cs]
fi_col = client[db_name][fi]


app = Flask(__name__)
Bootstrap(app)
CORS(app)


@app.route('/')
@app.route('/server_status', methods=['GET', 'POST'])
def server_status():
    return render_template("server_status_list.html")


@app.route('/command_history', methods=['GET', 'POST'])
def command_history():
    if request.method == "GET":
        id = request.args.get('id')
        id = str(id).zfill(3)
        dc_time = int(request.args.get('dc_time'))
        print(id)
        print(type(id))
        print(dc_time)
        print(type(dc_time))
        collect_time = {'collect_time': {'$lte': dc_time}}
        ch_data = list(ch_col.find(
            {'$and': [{'id': id}, {'collect_time': {'$lte': dc_time}}]}, {'_id': 0}))
        cs_data = list(cs_col.find(
            {'$and': [{'id': id}, {'collect_time': {'$lte': dc_time}}]}, {'_id': 0}))

        fi_data = list(fi_col.find(
            {'$and': [{'id': id}, {'committed_date': {'$lte': dc_time}}]}, {'_id': 0}))
        # for d in data:
        #     print(d)
        # print(data)
        # print(data2)
        res = {'command_history': ch_data,
               'command_script': cs_data, 'file_edit': fi_data}
        # res = jsonify(res)

        return render_template("command_history_list.html", res=res)
        # return res


@app.route('/api/server_status', methods=['GET', 'POST'])
def api_server_status():
    if request.method == "GET":
        group = st_col.distinct('group')

        find_res = list(st_col.find({'group': group[0]}))
        # print(find_res)
        collection_time = list(set([v['collection_time'] for v in find_res]))

        steps = st_col.distinct('step')
        status = {'group': group,
                  'collection_time': collection_time, 'steps': steps}
        return jsonify(status)

    elif request.method == "POST":
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
            if doc['stdout'] == 'nan':
                doc['stdout'] = 'N/A'
        
            if doc['stderr'] == 'nan':
                doc['stderr'] = 'N/A'



            data[0].append({'id': doc['id'], 'host': doc['host'], 'collection_time': doc['collection_time'], 'command': doc['command'],
                            'stdout': doc['stdout'], 'stderr': doc['stderr'], 'detail_collection_time': doc['detail_collection_time']})

        data[1].append(analysis)
        # print(rows)
        # print(type(testdata))
        return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
