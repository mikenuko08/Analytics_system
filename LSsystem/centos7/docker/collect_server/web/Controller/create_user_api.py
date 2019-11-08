# coding: utf-8
import os

from flask import Flask, abort, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

Users = [
    {'id': 1, 'name': 'aaa'},
    {'id': 2, 'name': 'bbb'},
    {'id': 3, 'name': 'ccc'},
    {'id': 4, 'name': 'ddd'},
    {'id': 5, 'name': 'eee'},
]


class User(Resource):
    def get(self):
        return

    def put(self):
        return

    def delete(self):
        return


class Users(Resource):
    def get(self):
        return

    def post(self):
        return

    def put(self):
        return

    def delete(self):
        return


api.add_resource(User, '/api/users/<int:id>')
api.add_resource(Users, '/api/users')

if __name__ == "__main__":
    app.run(debug=True)
