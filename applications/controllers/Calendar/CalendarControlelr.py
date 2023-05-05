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

class Calendars (Resource):
    def post(self,id):
       try:
           new_calendar = Calendar()
           db.session.add(new_calendar)
           db.session.commit()
           
           new_creation_event = Creation_event(project_id = id, calendar_id = new_calendar.id )
           db.session.add(new_creation_event)
           db.session.commit()

           return  {"ID" : new_calendar.id }
       
       except Exception as e:
           return {"Error Message" : str(e)},400
       
       finally:
           db.session.close()
    def delete(self,id):
        try:
            db.session.delete(Calendar.query.filter_by(id = id))
            db.session.commit()
            return {"Message" : "managed to delete!"},200
        except Exception as e:
            return {"message" : str(e)}
        finally:
            db.session.close()

@api.route("/task/<int:id>")
@api.produces('application/json')
class Calendar_Task(Resource):
    def post (self,id):
        try:
            info = request.json
            name = info.get("name")
            due_date = datetime.utcnow()
            print(due_date)
            calendar_id = id 
            if not all ([name,due_date,calendar_id]):
                raise ValueError("Missing Field, either misspelt or other")
            new_task =  Calendar_task(name = name,due_date = due_date,calendar_id = calendar_id)
            db.session.add(new_task)
            db.session.commit()
            return {"ID" : new_task.id },200
        except Exception as e:
            return {"message" : str(e)},200
        finally:
            db.session.close()