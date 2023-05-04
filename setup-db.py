from applications import create_app
from applications.database import db
from applications.model.model import user_account

db = SQLAlchemy()

def create_database():
    with create_app().app_context():
        db.init_app(create_app())
        db.create_all()


def delete_database():
    with create_app.app_context():
        db.drop_all()
        
def add_entries():
    admin = user_account(username = "Hello", password = "password123",email = "helloworld@gmail.com",name = "Fil", skill_level = 0,skills = "",role = "")
    with create_app.app_context():
        db.session.add(admin)
        db.session.commit()

def see_db():
    with create_app.app_context():
        with create_app.app_context():
            entries = user_account.query.all()
            for entry in entries:
                print(f"{entry.username}, {entry.password}")

if __name__ == "__main__":
    delete_database()
    create_database()
    add_entries()
    see_db()
