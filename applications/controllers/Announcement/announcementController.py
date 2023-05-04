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