from applications import db,app
from datetime import datetime

class Kanban_board(db.Model):
    __tablename__ = 'kanban_board'
    id = db.Column(db.integer,primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    categories = db.Column(db.String,nullable = True)

class Kanban_task(db.Model):
    __tablename__ = "kanban_task"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable = False)
    category = db.Column(db.string,nullable = False)
    objective = db.Column(db.string,nullable = False)
    kanban_id = db.Column(db.Integer,db.ForeignKey('kanban_board'))

class Calendar(db.Model):
    __tablename__ = 'calendar'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable = False)

class Calendar_task(db.Model):
    __tablename__ = "calendar_task"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable = False)
    due_date = db.Column(db.DateTime(), default = datetime.utcnow)
    calendar_id = db.Column(db.Integer,db.ForeignKey('calendar.id'))

class Creation_event(db.Model):
    __tablename__ = "creation_event"
    id = db.Column(db.Integer, primary_key = True)
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))
    kanban_id = db.Column(db.Integer,db.ForeignKey('kanban_board.id'))
