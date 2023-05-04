from applications import  create_app
from applications.database import db
from flask import request, jsonify
from flask_restx import Namespace, Resource

api = Namespace('calendar', description='calendar operations')