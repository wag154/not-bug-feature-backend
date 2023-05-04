def init_model(db_instance):
    import dotenv
    import os
    from .model import user_account, Kanban_board, Kanban_task, \
        Calendar, Calendar_task, Creation_event, Project, Announcement, ProjectMember
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    if (os.getenv("restart_db") == "1"):
        try:
            db_instance.drop_all()
            dotenv.set_key(dotenv_file,"restart_db","0")
        except:
            print("unable to check")
    db_instance.create_all()
