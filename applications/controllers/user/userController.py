from flask import request, make_response
from applications.model.model import user_account as UserModel
from applications.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restx import Namespace, Resource
import uuid
from sqlalchemy import exc
import jwt
import datetime
from functools import wraps

api = Namespace('users', description='user operations')
db = db.instance


def auth_decorator(f):
    @wraps(f)
    def wrapped(self, *args, **kwargs):
        token = None
        print(token)

        # Backend will expect to receive the token as a header under this key.
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {"message": "Token is missing."}, 401

        try:
            data = jwt.decode(token, "secret", algorithms="HS256")
            current_user = UserModel.query.filter_by(public_id=data['public_id']).first()

        except Exception as e:
            print(e)
            return {"message": "Invalid token."}

        return f(self, current_user, *args, **kwargs)

    return wrapped


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


@api.route('/<string:username>')
class User(Resource):
    @auth_decorator
    def patch(self, current_user, username):
        user = UserModel.query.filter_by(username=username).first()

        if not user:
            return {"message": "Invalid username."}

        data = request.get_json()

        user.name = data['name']
        user.skill_level = data['skill_level']
        user.skills = data['skills']
        user.role = data['role']
        db.session.commit()

        return {"message": "User details successfully updated."}, 202

    @auth_decorator
    def get(self, current_user, username):
        user = UserModel.query.filter_by(username=username).first()

        if not user:
            return {"message": "User not found."}, 404

        user_data = {'public_id': user.public_id,
                     'username': user.username,
                     'email': user.email,
                     'name': user.name,
                     'skill_level': user.skill_level,
                     'skills': user.skills,
                     'role': user.role}

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
            token = jwt.encode({'public_id': user.public_id,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
                               "secret",
                               algorithm="HS256")

            return {"message": "Access granted.",
                    "public_id": user.public_id,
                    "token": token}, 200

        return make_response('Could not verify.', 401)
