from applications import app,db
from applications.model import Project
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

        return {"message": "Project created successfully."}, 201

    except ValueError as e:
        return {"message": str(e)}, 400

    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 500

    finally:
        db.session.close()

