from applications import  create_app
from applications.database import db
from applications.model.model import Kanban_board,Creation_event, Kanban_task
from flask import request, jsonify
from flask_restx import Namespace, Resource

api = Namespace('kanban', description='kanban operations')
db = db.instance

@api.route('/<int:id>')
@api.produces('application/json')
class Kanban (Resource):
    def get (self,id):
        try :
             project_id = id
             get_kanban_id = Creation_event.query.filter_by(project_id = project_id).first()
             all_tasks = Kanban_task.query.filter_by(kanban_id = get_kanban_id.kanban_id).all()

             return {"success!":all_tasks}  
            
        except Exception as e:
            return {"message" :  str(e)}
        finally:
            db.session.close()
    def post (self,id):
         try:
            info = request.json
            name = info.get("name")
            categories = info.get("categories")
            project_id = id

            if not all([name,categories]):
                raise ValueError("Missing Fields")
            
            kanban = Kanban_board(name = name, categories = categories)
            db.session.add(kanban)
            db.session.commit()
            print(kanban.id, project_id)
            create = Creation_event(kanban_id=kanban.id, project_id = project_id)
            db.session.add(create)
            db.session.commit()
            print(kanban.id)
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
            
            edit_kanban = Kanban_board.query.get(get_kanban.kanban_id)
            
            if not edit_kanban:
                return {"message" : "unable to find kanban"}
            
            edit_kanban.name, edit_kanban.categories,edit_kanban.project_id = name, categories,project_id   
            print(edit_kanban)

            db.session.add(edit_kanban)
            db.session.commit()

            return {"Update successful!"}, 200
        except ValueError as e:
            return {"message" : str(e)}
        
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
            if not kanban:
              raise ValueError("Kanban board not found for project ID {}".format(project_id))

            db.session.delete(kanban)
            db.session.commit()

            return {"message": "Kanban board deleted successfully"}

         except Exception as e:
            return {"message": str(e)}
         
         finally:
             db.session.close()

            
@api.route("/task/<int:id>")
@api.produces('application/json')
class Task (Resource):
    def post(self, id):
        try:
            info = request.json
            name = info.get("name")
            category = info.get("category")
            objective = info.get("objective")
            kanban_id = id
            if not all ([name,category,objective,kanban_id]):
                raise ValueError("missing field")
            new_Task = Kanban_task(name = name, category = category, objective = objective, kanban_id = kanban_id)

            db.session.add(new_Task)
            db.session.commit()

            return {"list of info" : {new_Task.id, new_Task.name, new_Task.category} }, 200
        except Exception as e:
            return {"Message" : str(e)}, 404
        finally: 
            db.session.close()
    def put(self,id):
       try :
            info = request.json
            name = info.get("name")
            categories = info.get("categories")
            objective = info.get("objective")
            kanban_id = id

            if not all ([name,categories,objective,kanban_id]):
                raise ValueError ("Missing Field")
            kanban_task =Kanban_task.query.get(kanban_id)
            if not kanban_task:
                raise ValueError(f"Unable to get kanban task! task :{kanban_task}")

            kanban_task.name,kanban_task.categories,kanban_task.objective, = name ,categories,objective

            db.session.add(kanban_task)
            db.session.commit()

            return {"Update successful!"}, 200
       
       except ValueError as e:
            return {"message" : str(e)}
        
       except Exception as e:
            db.session.rollback()
            return {"message" : str(e)},500
       
       finally:
            db.session.close() 
    def delete(self,id):
        try:
            kanban_id = id
        
            remove_task = Kanban_task.query.filter_by(kanban_id=kanban_id).first()
            if not remove_task:
                raise ValueError("Couldn't find value!")

            db.session.delete(remove_task)
            db.session.commit()

            return {"message": "Kanban board deleted successfully"}

        except Exception as e:
            return {"message": str(e)}
         
        finally:
             db.session.close()