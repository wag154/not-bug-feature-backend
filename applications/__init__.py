from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://choatmvv:mCKh19dSOOvCYrtXDXELcS8SGJdiQ2Pc@horton.db.elephantsql.com/choatmvv"
app.config["SECRET_KEY"] = "pass"

db = SQLAlchemy(app)

from applications import route