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
