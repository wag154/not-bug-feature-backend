from applications import app,db
from applications.model import Project,Kanban_board,Creation_event,ProjectMember,Kanban_task,Announcement
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

@app.route("/kanban/card/<int:id>",methods = ["POST"])
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
@app.route("/announcement/<int:id>",methods = ["POST"])
def add_announcement(id):
    try:
        info = request.json
        username = info.get("username")
        title = info.get("title")
        message = info.get("message")
        pinned = (lambda a,b,c :a if (c == "true") else b )(True,False,info.get("pinned"))

        if not all ([username,title,message,pinned]):
            ValueError("Missing Field")
        
        new_announcement = Announcement(username = username, title = title, message = message, pinned = pinned)

        db.session.add(new_announcement)
        db.session.commit()

        return {"message" : "success!"}, 200
    
    except Exception as e:
        return {"Message" : str(e)}
    finally:
        db.session.close()
# from applications import app, db
# from flask import request, jsonify
# import uuid
# from applications.model.model import User
# from werkzeug.security import generate_password_hash
#
#
# @app.route('/')
# def hello():
#     return 'hello', 200
#
#
#
# @app.route('/user/<username>', methods=['GET'])
# def get_user_by_username(username):
#     user = User.query.filter_by(username=username).first()
#
#     if not user:
#         return jsonify({"message": "Invalid username."})
#
#     user_data = {}
#     user_data['public_id'] = user.public_id
#     user_data['username'] = user.username
#     user_data['password'] = user.password
#     user_data['email'] = user.email
#
#     return jsonify({"user": user_data})
#
#
# @app.route('/register', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     # will receive a json object containing username, password and email from frontend.
#     hashed_password = generate_password_hash(data['password'], method='sha256')
#     # generating a public id and creating new user.
#     new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password,
#                     email=data['email'])
#     db.session.add(new_user)
#     db.session.commit()
#
#     return jsonify({"message": "New user created."}), 201
#
#
# @app.route('/user/<username>', methods=['PATCH'])
# def update_user(username):
#     user = User.query.filter_by(username=username).first()
#
#     if not user:
#         return jsonify({"message": "Invalid username."})
#
#     data = request.get_json()
#
#     user.name = data['name']
#     user.skill_level = data['skill_level']
#     user.skills = data['skills']
#     user.role = data['role']
#     db.session.commit()
#
#     return jsonify({"message": "User details successfully updated."})
#
# # /login
# # /logout
