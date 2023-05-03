from applications import app,db
from applications.model import Project,Kanban_board,Creation_event,ProjectMember,Kanban_task
from flask import request
import jsonify
@app.route('/')
def hello():
    return 'hello', 200

@app.route("/project", methods=["POST"])
def create_project():
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
        print("here")
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

@app.route("/kanban/<int:id>", methods = ["POST"])
def create_kanban (id):
    try:
        info = request.json
        name = info.get("name")
        categories = info.get("categories")
        if not all([name,categories]):
            raise ValueError("Missing Fields")
        kanban = Kanban_board(name = name, categories = categories)
        db.session.add(kanban)
        db.session.commit()
        create = Creation_event(kanban_id=kanban.id)
        db.session.add(create)
        db.session.commit()
        return {"kanban ID" : kanban.id} , 200
    except Exception as e:
        return {"message" : str(e)}
        
    finally:
            db.session.close()
@app.route("/teammember/<int:id>", methods = ["POST"])
def add_teamMember (id):
    try:
        info = request.json
        level = info.get("level")
        role = info.get("role")
        user_id = info.get("user_id")
        project_id = id
        if not all ([level,role,user_id,project_id]):
            raise ValueError()
        new_team_member = ProjectMember(level = level, role = role, user_id = user_id,project_id = project_id)
        db.session.add(new_team_member)
        db.session.commit()
        return {"message":"success!"}, 200
    except Exception as e:

        return {"message" : str(e)}
    finally:
        db.session.close()

@app.route("/kanban/card/<int:id>")
def create_card(id):
    try:
        info = request.json
        name = info.get("name")
        category = info.get("category")
        objective = info.get("objective")
        kanban_id = id
        if not all ([name,category,objective,kanban_id]):
            raise ValueError("Missing field")
        card = Kanban_task(name = name, categories = category,objective = objective,kanban_id = kanban_id)
        
        db.session.add(card)
        db.session.commit()

        return {"message" : "success!"}, 200
    
    except Exception as e:
        return {"Message" : str(e)}
    finally:
        db.session.close()
