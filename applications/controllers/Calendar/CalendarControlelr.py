from applications import  create_app
from applications.database import database_service
from applications.model.model import Calendar,Calendar_task,Creation_event
from flask import request, jsonify
import json
from flask_restx import Namespace, Resource
from datetime import datetime

api = Namespace('Calendar', description='Calendar operations')
db = database_service.instance

@api.route("/<int:id>")
@api.produces('application/json')

class Calendars (Resource):
    def get(self,id):
        try:
            get_id = [event for event in Creation_event.query.filter_by(project_id=id).all() if event.calendar_id is not None]

            return {"id" : get_id[0].id},200
        
        except Exception as e:
            return {"message": str(e)},404
    def post(self,id):
       try:
           test_id = Creation_event.query.filter_by(project_id = id).all()
           for i in test_id:
              if i and i.calendar_id:
                 return {"message": "calendar already exists"},409
            
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


            cal = Calendar.query.filter_by(id = id).first()
            all_tasks = Calendar_task.query.filter_by(calendar_id = cal.id).all()
            for i in all_tasks:
                db.session.delete(i)
            db.session.commit()

            creation = Creation_event.query.filter_by(calendar_id = cal.id).first()
            db.session.delete(creation)
            db.session.commit()
            db.session.delete(cal)
            db.session.commit()
            return {"Message" : "managed to delete!"},200
        except Exception as e:
            return {"message" : str(e)},404
        finally:
            db.session.close()

@api.route("/task/<int:id>")
@api.produces('application/json')
class Calendar_Task(Resource):
    def get (self,id):
        try:
            calendar_id = id
            all_tasks = Calendar_task.query.filter_by(calendar_id = calendar_id).all()
            send_list = [
                    {
                     "id": task.id,
                     "name": task.name,
                     "calendar_id": task.calendar_id,
                     "complete": task.complete,
                     "due_date": task.due_date.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    for task in all_tasks
                  ] 

            serialised_send_list = json.dumps(send_list)
            return jsonify({"All Tasks":serialised_send_list}),200

        except Exception as e:
            return {"message" : str(e)}
    def post (self,id):
        try:
            info = request.json
            name = info.get("name")
            complete_str = info.get("complete")
            due_date_str = info.get("due_date")
            calendar_id = id 
            if not all ([name,due_date_str,calendar_id,complete_str]):
                raise ValueError("Missing Field, either misspelt or other")
            complete = (lambda a,b,c :a if (c == "true") else b )(True,False,complete_str)
            without = due_date_str.split(".")[0]
            due_date = datetime.strptime(without, '%Y-%m-%d %H:%M:%S')

            new_task = Calendar_task(complete = complete, name = name,due_date = due_date,calendar_id = calendar_id)
            db.session.add(new_task)
            db.session.commit()

            return {"ID" : new_task.id },200
        except Exception as e:
            return {"message" : str(e)},400
        finally:
            db.session.close()

    def put(self,id):
        try:
            info = request.json
            name = info.get("name")
            complete_str = info.get("complete")
            due_date_str = info.get("due_date")

            calendar_task_id = id
            if not all ([name,due_date_str,calendar_task_id,complete_str]):
                raise ValueError("Missing Field, either misspelt or other")
            complete = (lambda a,b,c :a if (c == "true") else b )(True,False,complete_str)
            without = due_date_str.split(".")[0]
            due_date = datetime.strptime(without, '%Y-%m-%d %H:%M:%S')

            update_task = Calendar_task.query.filter_by(id = id ).first()
            update_task.name = name
            update_task.due_date = due_date
            update_task.complete = complete

            db.session.commit()

            return {"message" : "success!"},200
        except Exception as e:
            return {"message":str(e)},400
        finally:
            db.session.close()
    def delete (self,id):
        try:
            task_id = id
            get_task = Calendar_task.query.filter_by(id = task_id).first()
            db.session.delete(get_task)
            db.session.commit()
            return {"message":"success!"}, 201
        except Exception as e:
            return {"message" : str(e)}
        finally:
            db.session.close()