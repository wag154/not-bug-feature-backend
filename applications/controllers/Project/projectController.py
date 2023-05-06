from applications import  create_app
from applications.database import db
from applications.model.model import Project,Creation_event,Calendar,Calendar_task,ProjectMember,Kanban_task,Kanban_board,Announcement
from flask import request, jsonify
from flask_restx import Namespace, Resource

api = Namespace('Project', description='Project operations')
db = db.instance

@api.route('/<int:id>')
@api.produces('application/json')
class project(Resource):
    def get (self,id):
        try:
            get_all_for_user = Project.query.filter_by(user_id = id).all()
            print(get_all_for_user)
            if not get_all_for_user:
                raise ValueError("This User Current Has No Projects!")
            
            return_list = [i.to_dict() for i in get_all_for_user]
            return {"user projects" : return_list},200
        except Exception as e:
            return {"message" :str(e)},400
    def post(self,id):
        try:
            info = request.json
            title = info.get("title")
            description = info.get("description")
            tech_stack = info.get("tech_stack")
            positions = info.get("positions")
            user_id = info.get("user_id")
            duration = info.get("duration")
            chatroom_key = info.get("chatroom_key")
            num_of_collaborators = info.get("number_of_collaborators")

            if not all([title, description, tech_stack, positions, user_id, duration, num_of_collaborators,chatroom_key]):
                raise ValueError("Missing fields")
        
            project = Project(
             title=title,
            description=description,
            tech_stack=tech_stack,
            positions=positions,
            user_id=user_id,
            duration=duration,
            number_of_collaborators=int(num_of_collaborators),
            chatroom_key = chatroom_key
        )
            db.session.add(project)
            db.session.commit()

            return {"Project ID": project.id,"Chatroom_key" : chatroom_key}, 201
    
        except ValueError as e:
          return {"message": str(e)}, 400

        except Exception as e:
           db.session.rollback()
           return {"message": str(e)}, 500

        finally:
             db.session.close()
    def put(self,id):
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

            update_project = Project.query.filter_by(user_id = user_id,id = id).first()
            update_project.title, update_project.description, update_project.tech_stack,update_project.positions,update_project.user_id, update_project.duration,update_project.number_of_collaborators = title,description,tech_stack,positions,user_id,duration,num_of_collaborators

            db.session.commit()

            return {"Message" : "Success!"},200
        except Exception as e:
            return {"message" : str(e)},400
        finally:
            db.session.close()
            
    def delete(self,id):
        try:     
            remove_project = Project.query.filter_by(id = id).first()
            all_creation_event = Creation_event.query.filter_by(project_id = id).all()
            for i in all_creation_event:
                if i.calendar_id:
                    new_cal = Calendar.query.filter_by(id = i.calendar_id).first()
                    all_tasks = Calendar_task.query.filter_by(calendar_id = i.calendar_id).all()
                    certain_event = Creation_event.query.filter_by(calendar_id = i.calendar_id, project_id = id).first()

                    for i in all_tasks:
                        db.session.delete(i)
                    db.session.commit()
                    db.session.delete(certain_event)
                    db.session.commit()
                    db.session.delete(new_cal)
                    db.session.commit()

                elif i.project_member_id:
                    new_meb = ProjectMember.query.filter_by(id = i.project_member_id).first()
                    certain_event1 = Creation_event.query.filter_by(project_member_id = i.project_member_id, project_id = id).first()
                    db.session.delete(certain_event1)
                    db.session.commit()
                    db.session.delete(new_meb)
                    db.session.commit()

                elif i.kanban_id:
                    new_kanban = Kanban_board.query.filter_by(id = i.kanban_id).first()
                    all_task = Kanban_task.query.filter_by(kanban_id = i.kanban_id).all()
                    certain_event2 = Creation_event.query.filter_by(kanban_id = i.kanban_id, project_id = id).first()
                    for i in all_task:
                        db.session.delete(i)
                    db.session.commit()
                    db.session.delete(certain_event2)
                    db.session.commit()
                    db.session.delete(new_kanban)
                    db.session.commit()

                elif i.announcement_id:
                    get_announcement = Announcement.query.filter_by(id = i.announcement_id).first()
                    certain_event3 = Creation_event.query.filter_by(announcement_id = i.announcement_id, project_id = id).first()
                    db.session.delete(certain_event3)
                    db.session.commit()
                    db.session.delete(get_announcement)
                    db.session.commit()
                else:
                    get_project_id = Creation_event.query.filter_by(project_id = id).first()
                    db.session.delete(get_project_id)
                    db.session.commit()
            db.session.commit()
            db.session.delete(remove_project)
            db.session.commit()
        
            return {"Message": "success"},200
        except Exception as e:
            return {"Message" : str(e)},400
        finally:
            db.session.close()