from applications import app,db
from applications.model import Project
from sqlalchemy import update,delete,insert
from flask import request
@app.route('/')
def hello():
    return 'hello', 200

@app.route("/project", methods = ["POST"])
def create_project():
    info = request.json
    try :
        title = info["title"]
        description = info["description"]
        tech_stack = info["tech_stack"]
        pos = info["position"]

        new_project = Project(title,description,tech_stack,pos)

        db.session.add(new_project)
        db.session.commit()

        return 200
    except:
        return "check keynames",404
