from applications import  create_app
from applications.database import db
from applications.model.model import Calendar,Calendar_task,Creation_event
from flask import request, jsonify
from flask_restx import Namespace, Resource
from datetime import datetime

api = Namespace('calendar', description='calendar operations')
db = db.instance

@api.route("/<int:id>")
@api.produces('application/json')

class Calendar (Resource):
    def post(self,id):
       try:
           info = request.json
           name = info.get("name")

           if not name:
               raise ValueError("Missing 'name'")
           
           new_calendar = Calendar(name = name)
           db.session.add(new_calendar)
           db.session.commit()
           
           new_creation_event = Creation_event(project_id = id, calendar_id = new_calendar.id )
           db.session.add(new_creation_event)
           db.session.commit()
           
       except Exception as e:
           return {"Error Message" : str(e)}
       
       finally:
           db.session.close()