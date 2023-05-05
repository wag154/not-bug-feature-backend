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
