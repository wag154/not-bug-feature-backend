from applications import  create_app
from applications.database import db
from flask import request, jsonify
from flask_restx import Namespace, Resource
from applications.model.model import Announcement,Creation_event

api = Namespace('announcement', description='announcement operations')
db = db.instance

@api.route("/<int:id>")
@api.produces('application/json')
class Announcements (Resource):
    def get(self,id):
        try:

            project_id = id 
            get_announcement_id = Creation_event.query.filter_by(project_id = project_id).all()
            all_id = [i.id for i in get_announcement_id]
            all_announcements = [Announcement.query.filter_by(id = id).all() for id in all_id]
            if not all_announcements or all_announcements==None:
                raise ValueError("Not announcements")
            send_list = []
            for i in all_announcements:
                child = [a.to_dict() for a in i]
                send_list.append(child)
            return {"All Announcement" : f"{send_list}"}

        except Exception as e:
            return {"message": str(e)}

    def post (self,id):
        try:
           info = request.json
           username = info.get("username")
           title = info.get("title")
           message = info.get("message")
           pinned = info.get("pinned")
           if not all ([username,title,message,pinned]):
               raise ValueError("Missing field")
           
           pinned = (lambda a,b,c :a if (c == "true") else b )(True,False,pinned)
           new_announcement = Announcement(username = username, title = title,message = message,pinned = pinned)
           db.session.add(new_announcement)
           db.session.commit()

           new_create_event = Creation_event(project_id = id, announcement_id = new_announcement.id)
           db.session.add(new_create_event)
           db.session.commit()

           return {"id": new_announcement.id},200
        
        except Exception as e :
            return {"message" : str(e)},400
        finally:
            db.session.close()

    def put (self,id):
        try:
           info = request.json
           username = info.get("username")
           title = info.get("title")
           message = info.get("message")
           pinned = info.get("pinned")
           announcement_id = id

           if not all ([username,title,message]) and pinned != None or pinned == "":
               raise ValueError("Missing field")
           
           pinned = (lambda a,b,c :a if (c == "true") else b )(True,False,pinned)
           
           edit_announcement = Announcement.query.filter_by(id = announcement_id).first()
           
           edit_announcement.username,edit_announcement.title,edit_announcement.message,edit_announcement.pinned = username,title,message,pinned
           db.session.commit()
           return {"message" : "success"}
        
        except Exception as e:
            return {"message" : str(e)},400
        finally:
            db.session.close()

    def delete (self,id):
        try:
            info = request.json
            get_create_event = Creation_event.query.filter_by(announcement_id = id).first()
            print(get_create_event)
            db.session.delete(get_create_event)
            db.session.commit()

            remove_announcement = Announcement.query.filter_by(id = id).first()
            db.session.delete(remove_announcement)
            db.session.commit()
        
            return {"success", "message"}
        except Exception as e:
            return {"message" : str(e)},400
        finally:
            db.session.close()