from applications import db, app
from applications.model import User
#from applications.models import 

def create_database():
    with app.app_context():
        db.create_all()

def delete_database():
    with app.app_context():
        db.drop_all()
def add_entries():
    admin = User(username = "Hello", password = "password123",email = "helloworld@gmail.com",name = "Fil", skill_level = 0,skills = "",role = "")
    with app.app_context():
        db.session.add(admin)
        db.session.commit()
def see_db():
    with app.app_context():
        with app.app_context():
            entries = User.query.all()
            for entry in entries:
                print(f"{entry.username}, {entry.password}")

if __name__ == "__main__":
    delete_database()
    create_database()
    add_entries()
    see_db()