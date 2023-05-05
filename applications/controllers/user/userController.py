from flask import request, jsonify, make_response
from applications.model.model import user_account as UserModel
from applications.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restx import Namespace, Resource
import uuid
from sqlalchemy import exc

api = Namespace('users', description='user operations')
db = db.instance


@api.route('/')
class User(Resource):
    def get(self):
        return 'hello', 200

    def post(self):
        data = request.get_json()
        try:
            # will receive a json object containing username, password and email from frontend.
            hashed_password = generate_password_hash(data['password'], method='sha256')

            # # generating a public id and creating new user.
            new_user = UserModel(public_id=str(uuid.uuid4()),
                                 username=data['username'],
                                 password=hashed_password,
                                 email=data['email'])

            db.session.add(new_user)
            db.session.commit()
            return {"message": "New user created.", "public_id": f"{new_user.public_id}"}, 201

        except KeyError:
            return {"message": "Invalid information."}, 500

        except exc.IntegrityError:
            return {"message": "Username or email already exist."}, 500


@api.route('/<string:public_id>')
class User(Resource):
    def patch(self, public_id):
        user = UserModel.query.filter_by(public_id=public_id).first()

        if not user:
            return {"message": "Invalid username."}

        data = request.get_json()

        user.name = data['name']
        user.skill_level = data['skill_level']
        user.skills = data['skills']
        user.role = data['role']
        db.session.commit()

        return {"message": "User details successfully updated."}

    def get(self, public_id):
        user = UserModel.query.filter_by(public_id=public_id).first()

        if not user:
            return {"message": "User not found."}, 404

        user_data = {'public_id': user.public_id, 'username': user.username, 'password': user.password,
                     'email': user.email}

        return {"user": user_data}, 200


@api.route('/login')
class User(Resource):
    def get(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('Invalid credentials.', 401)

        user = UserModel.query.filter_by(username=auth.username).first()

        if not user:
            return make_response('Invalid username.', 401)

        if check_password_hash(user.password, auth.password):
            print('it works')
            print(user.public_id)
            return make_response(f'Access granted. {user.public_id}', 200)

        return make_response('Could not verify.', 401)
