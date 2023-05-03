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


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=True)
    skill_level = db.Column(db.String(100), nullable=True)
    skills = db.Column(db.String(500), nullable=True)
    role = db.Column(db.String(100), nullable=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    
    def __repr__(self):
        return f"username: {self.username}\nemail: {self.email}\npassword: {self.password}"


class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    number_of_collaborators = db.Column(db.Integer, nullable=False)
    tech_stack = db.Column(db.String(500), nullable=False)
    positions = db.Column(db.String(500), nullable=False)

    def __init__(self, title, description, duration, number_of_collaborators, tech_stack, positions):
        self.title = title
        self.description = description
        self.duration = duration
        self.number_of_collaborators = number_of_collaborators
        self.tech_stack = tech_stack
        self.positions = positions
    
    def __repr__(self):
        return f"title: {self.title}\ndescription: {self.description}\nduration: {self.duration}\nnumber of collaborators: {self.number_of_collaborators}\ntech stack: {self.tech_stack}\npositions: {self.positions}"


class Announcement(db.Model):
    __tablename__ = "announcement"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=True, default='')
    pinned = db.Column(db.Boolean, server_default='t', default=False)

    def __init__(self, username, title, message, pinned):
        self.username = username
        self.title = title
        self.message = message
        self.pinned = pinned

    def __repr__(self):
        return f"username: {self.username}\ntitle: {self.title}\nmessage: {self.message}\npinned: {self.pinned}"


class ProjectMember(db.Model):
    __tablename__ = "projectMember"

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer,db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self, level, role):
        self.level = level
        self.role = role
    
    # Not returning a string representation for this model since it would require a join to make sense.
