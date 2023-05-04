from flask import request, jsonify
from applications.model.model import user_account as UserModel
from applications.database import db
from werkzeug.security import generate_password_hash
from flask_restx import Namespace, Resource
import uuid

api = Namespace('users', description='user operations')
db = db.instance


@api.route('/')
class User(Resource):
    def get(self):
        return 'hello', 200

    def post(self):
        data = request.get_json()
        # will receive a json object containing username, password and email from frontend.
        hashed_password = generate_password_hash(data['password'], method='sha256')

        # # generating a public id and creating new user.
        new_user = UserModel(public_id=str(uuid.uuid4()),
                             username=data['username'],
                             password=hashed_password,
                             email=data['email'])

        db.session.add(new_user)
        db.session.commit()
        return {"message": "New user created."}, 201

# Make similar to https://github.com/tsungtwu/flask-example/blob/master/webapp/app/api/user/apiController.py#L71
# need to create a route @api.route('/<string:id>') and add a get and put methods equal to the link above

# @api.route('/user/<username>', methods=['GET'])
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
# @api.route('/register', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     # will receive a json object containing username, password and email from frontend.
#     # hashed_password = generate_password_hash(data['password'], method='sha256')
#     # # generating a public id and creating new user.
#     # new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password,
#     #                 email=data['email'])
#     # db.session.add(new_user)
#     # db.session.commit()
#
#     return jsonify({"message": "New user created."}), 201
#
#
# @api.route('/user/<username>', methods=['PATCH'])
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
#     # db.session.commit()
#
#     return jsonify({"message": "User details successfully updated."})

# /login
# /logout
