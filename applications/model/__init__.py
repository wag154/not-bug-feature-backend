def init_model(db_instance):
    from .model import User, Kanban_board, Kanban_task, \
        Calendar, Calendar_task, Creation_event, Project, Announcement, ProjectMember
    db_instance.create_all()
