from applications import  create_app
from applications.database import db
from applications.model.model import ProjectMember,Creation_event
from flask import request, jsonify
from flask_restx import Namespace, Resource

api = Namespace('TeamMember', description='TeamMember operations')
db = db.instance

@api.route("/<int:id>")
@api.produces('application/json')
class TeamMember(Resource):
    def post (self,id):
        try:
            info = request.json
            level = info.get("level")
            role = info.get("role")
            user_id = info.get("user_id")
            project_id = id

            if not all ([level,role,user_id,project_id]):
                raise ValueError("Missing field")
            
            new_member = ProjectMember(level = level, role = role, user_id = user_id,project_id = project_id)
            db.session.add(new_member)
            db.session.commit()

            new_creation_event = Creation_event(project_id = project_id,)

            
        except Exception as e:
             return {"message" : str(e)}
