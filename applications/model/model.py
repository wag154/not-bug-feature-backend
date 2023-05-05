from applications.database import db
from datetime import datetime

db = db.instance
class user_account(db.Model):
    __tablename__ = "user_account"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=True)
    skill_level = db.Column(db.String(100), nullable=True, default = "")
    skills = db.Column(db.String(500), nullable=True, default = "")
    role = db.Column(db.String(100), nullable=True, default = "")

class ProjectMember(db.Model):
    __tablename__ = "projectmember"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable = True)
    level = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer,db.ForeignKey('project.id',ondelete='CASCADE'), nullable =False )
    user_id = db.Column(db.Integer,db.ForeignKey('user_account.id'))

class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    number_of_collaborators = db.Column(db.Integer, nullable=False)
    tech_stack = db.Column(db.String(500), nullable=False)
    positions = db.Column(db.String(500), nullable=False)
    chatroom_key = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('user_account.id'))
    url = db.Column(db.String,nullable = True)

    def to_dict(self):
        return {
            "id" : self.id,

        }
class Kanban_task(db.Model):
    __tablename__ = "kanban_task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String, nullable=False)
    objective = db.Column(db.String, nullable=False)
    kanban_id = db.Column(db.Integer, db.ForeignKey('kanban_board.id'))

    def to_dict(self):
        return {
            'id' : self.id,
            'name' :self.name,
            "category" : self.category,
            "objective" : self.objective,
            "kanban_id" : self.kanban_id 
        }
class Kanban_board(db.Model):
    __tablename__ = 'kanban_board'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    categories = db.Column(db.String, nullable=True)

class Announcement(db.Model):
    __tablename__ = "announcement"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=True, default='')
    pinned = db.Column(db.Boolean, server_default='t', default=False)

class Calendar_task(db.Model):
    __tablename__ = "calendar_task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    due_date = db.Column(db.DateTime(), default=datetime.utcnow)
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))

class Calendar(db.Model):
    __tablename__ = 'calendar'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    create_date = db.Column(db.DateTime(),default = datetime.utcnow)
class Creation_event(db.Model):
    __tablename__ = "creation_event"
    id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'), nullable = True)
    kanban_id = db.Column(db.Integer, db.ForeignKey('kanban_board.id'),nullable = True)
    project_id = db.Column(db.Integer,db.ForeignKey('project.id'),nullable = True)
    announcement_id = db.Column(db.Integer, db.ForeignKey('announcement.id'))
    project_member_id = db.Column(db.Integer,db.ForeignKey('projectmember.id'))
