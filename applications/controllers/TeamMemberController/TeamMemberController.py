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
    def get (self):
        pass
    def post (self,id):
        try:
            info = request.json
            name = info.get("name")
            level = info.get("level")
            role = info.get("role")
            user_id = info.get("user_id")
            project_id = id

            if not all ([level,role,user_id,project_id,name]):
                raise ValueError("Missing field")
            
            new_member = ProjectMember(level = level, role = role, user_id = user_id,project_id = project_id)
            checker = ProjectMember.query.filter_by(user_id = int(user_id),project_id= project_id).first()
            print(checker)
            if checker:
                return {"Failed" : "user already is a member of this project!"}, 409
            
            new_creation_event = Creation_event(project_id = project_id,project_member_id = new_member.id)
            db.session.add(new_member)
            db.session.commit()
            print("here")
            db.session.add(new_creation_event)
            db.session.commit()
            return {"team_member_id" : new_member.id}
        
        except Exception as e:
             return {"message" : str(e)}, 400
        
        finally :
            db.session.close()

    def put (self,id):
        try:
            info = request.json
            level = info.get("level")
            role = info.get("role")
            user_id = info.get("user_id")
            project_id = id
            
            if not all ([level,role,user_id,project_id]):
                raise ValueError("Missing field")

            change_member_info = ProjectMember.query.filter_by(user_id = user_id, project_id = project_id).first()
 
            change_member_info.level, change_member_info.role = level , role 

            db.session.add(change_member_info)
            db.session.commit()

            return {"message" : "successful!"}
            
        except Exception as e:
            return {"message" : str(e)}
        finally:
            db.session.close()

    def delete (self,id):
        try:
            project_id = id
            info = request.json
            team_member_id = info.get("team_member_id")

            if not team_member_id or not project_id:
                raise ValueError("that id does not exist")
            team_member_event = Creation_event.query.filter_by(project_member_id = team_member_id, project_id = project_id).first()
            team_member = ProjectMember.query.filter_by(id = team_member_id).first()
            db.session.delete(team_member_event)
            db.session.commit()
            db.session.delete(team_member)
            db.session.commit()
        
            return {"Deletion":"Success!"},200
        except Exception as e:
            return {"message": str(e)}, 400
        finally:
            db.session.close()