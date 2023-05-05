def init_model(db_instance):
    import dotenv
    import os
    from sqlalchemy import text
    from .model import user_account, Kanban_board, Kanban_task, \
        Calendar, Calendar_task, Creation_event, Project, Announcement, ProjectMember
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    print(os.getenv("restart_db"))
    if (os.getenv("restart_db") == "1"):
        try:
            db_instance.session.execute(text('DROP TABLE IF EXISTS projectmember CASCADE;'))
            db_instance.session.execute(text('DROP TABLE IF EXISTS project CASCADE;'))
            db_instance.session.execute(text('DROP TABLE IF EXISTS user_account CASCADE;'))
            db_instance.session.commit()
            db_instance.drop_all()
            db_instance.create_all()
            db_instance.session.execute(text("INSERT INTO user_account(public_id,username,password,email,name,skill_level,skills,role) VALUES('123123adsadasd','admin123','password12asd3','email@gmasdail.com','john', 'junoir','python, js', 'being happy');"))
            db_instance.session.commit()
            db_instance.session.close()
            dotenv.set_key(dotenv_file,"restart_db","0")
        except Exception as e:
            print("An error occurred: ", e)

    db_instance.create_all()

