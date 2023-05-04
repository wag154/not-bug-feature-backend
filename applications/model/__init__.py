def init_model(db_instance):
    from .model import user_account, Kanban_board, Kanban_task, \
        Calendar, Calendar_task, Creation_event, Project, Announcement, ProjectMember
    print("Would you like to restart the db? [y]yes/[n]no")
    choice = str(input(":"))
    if choice == "y" :
        db_instance.drop_all()
    db_instance.create_all()