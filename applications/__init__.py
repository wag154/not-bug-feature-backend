from flask import Flask
from flask_cors import CORS
import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
        
        # url = os.getenv("DB_URL")
        
        # if 'postgresql' not in url:
        #     update_url = url.replace("postgres","postgresql")
        
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
        app.config["SECRET_KEY"] = "pass"

    # Initializing database
    from applications.database import database_service
    db.init_app(app)
    app.app_context().push()
    database_service.init_app(db)

    # Setting up CORS
    CORS(app)
    
    from applications.controllers import api
    api.init_app(app)

    return app
