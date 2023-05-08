from applications import  create_app
from applications.database import database_service
from flask import request, jsonify
from flask_restx import Namespace, Resource
import json
api = Namespace('Default', description='/default to get json of all required')
db = database_service.instance

@api.route('/')
@api.produces('application/json')
class hello(Resource):
    def get(self):
      
        with open("Doc/paths.json", "r") as f:
            data = json.load(f)
            print(data)

        return data
