from flask import Flask
from flask_cors import CORS

def create_app(env=None):
    app = Flask(__name__)

    if env == 'TEST':
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config["SECRET_KEY"] = "test"
    else:
        app.config["TESTING"] = False
        app.config["DEBUG"] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://choatmvv:mCKh19dSOOvCYrtXDXELcS8SGJdiQ2Pc@horton.db.elephantsql.com/choatmvv"
        app.config["SECRET_KEY"] = "pass"

    # Initializing database
    from applications.database import db
    app.app_context().push()
    db.init_app(app)
    CORS(app)
    
    from applications.controllers import api
    api.init_app(app)

    return app
