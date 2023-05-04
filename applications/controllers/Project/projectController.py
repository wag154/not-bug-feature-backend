from applications import  create_app
from applications.database import db
from applications.model.model import Project
from flask import request, jsonify
from flask_restx import Namespace, Resource

api = Namespace('project', description='project operations')
db = db.instance

@api.route('/')
@api.produces('application/json')
class project(Resource):
    def post(self):
        try:
            info = request.json
            title = info.get("title")
            description = info.get("description")
            tech_stack = info.get("tech_stack")
            positions = info.get("positions")
            user_id = info.get("user_id")
            duration = info.get("duration")
            num_of_collaborators = info.get("number_of_collaborators")

            if not all([title, description, tech_stack, positions, user_id, duration, num_of_collaborators]):
                raise ValueError("Missing fields")
        
            project = Project(
             title=title,
            description=description,
            tech_stack=tech_stack,
            positions=positions,
            user_id=user_id,
            duration=duration,
            number_of_collaborators=int(num_of_collaborators)
        )
            db.session.add(project)
            db.session.commit()

            return {"Project ID": project.id}, 201
    
        except ValueError as e:
          return {"message": str(e)}, 400

        except Exception as e:
           db.session.rollback()
           return {"message": str(e)}, 500

        finally:
             db.session.close()
