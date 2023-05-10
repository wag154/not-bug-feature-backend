from applications import  create_app
from applications.database import database_service
from applications.model.model import Kanban_board,Creation_event, Kanban_task
from flask import request, jsonify , make_response
from flask_restx import Namespace, Resource
import json

api = Namespace('Kanban', description='Kanban operations')
db = database_service.instance



@api.route('/<int:id>')
@api.produces('application/json')
class Kanban (Resource):
    def get (self,id):
        try :
            project_id = id
            get_kanban_id = [id for ce in Creation_event.query.filter_by(project_id=project_id)]
            if  len(get_kanban_id) == 0 :
                raise ValueError("Cannot find")
            kanban = Kanban_board.query.filter_by(id = get_kanban_id[0]).first()
            print(kanban)
            return {"ID" : kanban.id},200  
            
        except Exception as e:
            return {"message" :  str(e)} ,400
    def post (self,id):
         try:
            project_id = id
            test_id = Creation_event.query.filter_by(project_id = id).all()

            for i in test_id:
              if i and i.kanban_id:
                 return {"message": "kanban already exists"},409
            kanban = Kanban_board()
            db.session.add(kanban)
            db.session.commit()

            create = Creation_event(kanban_id=kanban.id, project_id = project_id)
            db.session.add(create)
            db.session.commit()
            print("id", kanban.id)
            return {"kanban ID" : kanban.id} , 200
         
         except Exception as e:
           return {"message" : str(e)},404
        
         finally:
             db.session.close()
    def put (self,id):
        try :
            info = request.json
            name = info.get("name")
            categories = info.get("categories")
            project_id = id

            if not all ([name,categories,project_id]):
                raise ValueError ("Missing Field")
            
            get_kanban = Creation_event.query.filter_by(project_id = id).first()
            if not get_kanban:
                return {"message" : "cannot be found"}, 404
            edit_kanban = Kanban_board.query.filter_by(id = get_kanban.kanban_id).first()

            if not edit_kanban:
                return {"message" : "unable to find kanban"}
            
            edit_kanban.name = name
            edit_kanban.categories = categories
            db.session.commit()

            return {"message":"Update successful!"}, 200
        except ValueError as e:
            return {"message" : str(e)},400
        
        except Exception as e:
            db.session.rollback()
            return {"message" : str(e)},500
        finally:
            db.session.close() 
    def delete(self, id):
         try:
            project_id = id
            
            get_kanban = Creation_event.query.filter_by(project_id = project_id).first()
            kanban = Kanban_board.query.get(get_kanban.kanban_id)

            get_creation_event = Creation_event.query.filter_by(kanban_id = get_kanban.kanban_id).first()
            db.session.delete(get_creation_event)
            all_tasks = Kanban_task.query.filter_by(kanban_id = get_kanban.kanban_id).all()



            for task in all_tasks:
                print(task)
                db.session.delete(task)
                db.session.commit()
            
            if not kanban:
              raise ValueError("Kanban board not found for project ID {}".format(project_id))
            db.session.delete(kanban)
            db.session.commit()

            return {"message": "Kanban board deleted successfully"},200

         except Exception as e:
            return {"message": str(e)},400
         
         finally:
             db.session.close()

@api.route("/task/<int:id>")
@api.produces('application/json')
class Task (Resource):
    def get (self,id):
        try :
            kanban_id = id
            all_tasks = Kanban_task.query.filter_by(kanban_id = kanban_id).all()
            send_list =[{"id" :task.id,"name" : task.name,"category":task.category,"objective":task.objective,"complete":task.complete} for task in all_tasks]
            return send_list, 200


        except Exception as e:
            return {"message" :  str(e)}, 404
        finally:
            db.session.close()
            
    def post(self, id):
        try:
            info = request.json
            required_fields = ["name", "category", "objective"]
            name = info.get("name")
            category = info.get("category")
            objective = info.get("objective")
            kanban_id = id
        
            missing_fields = [field for field in required_fields if field not in info]

            if missing_fields:
               raise ValueError("Missing fields: {}".format(", ".join(missing_fields)))            
            new_Task = Kanban_task(name = name, category = category, objective = objective, kanban_id = kanban_id)
            db.session.add(new_Task)
            db.session.commit()
            print("Yes?",new_Task.id)
            return {"task_id" : new_Task.id }, 200
        except Exception as e:
            print(str(e))
            return {"Message" : str(e)}, 404
        finally: 
            db.session.close()
    def put(self,id):
       try :
            info = request.json
            required_fields = ["name", "category", "objective"]
            name = info.get("name")
            categories = info.get("category")
            objective = info.get("objective")
            kanban_task_id = id

            missing_fields = [field for field in required_fields if field not in info]

            if missing_fields:
               raise ValueError("Missing fields: {}".format(", ".join(missing_fields))) 
            kanban_task =Kanban_task.query.filter_by(id = kanban_task_id).first()
            if not kanban_task:
                raise ValueError(f"Unable to get kanban task! task :{kanban_task}")
            kanban_task.name,kanban_task.category,kanban_task.objective,kanban_task.complete = name ,categories,objective
            db.session.commit()

            return {"message": "success!"}, 200
       
       except ValueError as e:
            return {"message" : str(e)}
        
       except Exception as e:
            db.session.rollback()
            return {"message" : str(e)},500
       
       finally:
            db.session.close() 
    def delete(self,id):
        try:
            kanban_task_id = id
            remove_task = Kanban_task.query.filter_by(id=kanban_task_id).first()
            if not remove_task:
                raise ValueError("Couldn't find task!")

            db.session.delete(remove_task)
            db.session.commit()

            return {"message": "Kanban board deleted successfully"},200

        except Exception as e:
            return {"message": str(e)},400
         
        finally:
             db.session.close()