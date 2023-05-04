from applications import  create_app
from applications.database import db
from flask import request, jsonify
from flask_restx import Namespace, Resource

api = Namespace('default', description='default operations')
db = db.instance

@api.route('/')
@api.produces('application/json')
class hello(Resource):
    def get(self):
        print("here")
        return {'message': 'hello world'}
