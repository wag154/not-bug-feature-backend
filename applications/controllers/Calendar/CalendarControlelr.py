from applications import  create_app
from applications.database import db
from flask import request, jsonify
from flask_restx import Namespace, Resource
from datetime import datetime

api = Namespace('calendar', description='calendar operations')
db = db.instance

@api.route("/<int:id>")
@api.produces('application/json')

class Calendar (Resource):
    def post(self):
       pass
