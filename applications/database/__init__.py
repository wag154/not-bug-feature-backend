from flask_sqlalchemy import SQLAlchemy
from applications.model import init_model


class DatabaseService:
    instance = None

    def __init__(self):
        pass

    def init_app(self, app):
        self.instance = SQLAlchemy(app)
        init_model(self.instance)


db = DatabaseService()
