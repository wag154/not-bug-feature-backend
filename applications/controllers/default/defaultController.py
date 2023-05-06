from applications import  create_app
from applications.database import database_service
from flask import request, jsonify
from flask_restx import Namespace, Resource

api = Namespace('default', description='default operations')
db = database_service.instance

@api.route('/')
@api.produces('application/json')
class hello(Resource):
    def get(self):
        print("here")
        return {'message': 'hello world'}
