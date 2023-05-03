from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://wswmkcmq:QgR_x3VkT-x3T7RbY37jXwJW1MHtm0BT@manny.db.elephantsql.com/wswmkcmq"
app.config["SECRET_KEY"] = "pass"

db = SQLAlchemy(app)

from applications import route