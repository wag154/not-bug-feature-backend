from flask_restx import Api

from applications.controllers.user.userController import api as user_controller


api = Api(title='My API')


api.add_namespace(user_controller, path='/user')