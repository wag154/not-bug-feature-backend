from flask_restx import Api

from applications.controllers.user.userController import api as user_controller
from applications.controllers.default.defaultController import api as default_controller
from applications.controllers.Kanban.kanbanController import api as kanban_controller
from applications.controllers.Calendar.CalendarControlelr import api as calendar_controller
from applications.controllers.Project.projectController import api as project_controller
from applications.controllers.TeamMemberController.TeamMemberController import api as TeamMemberController
from applications.controllers.Announcement.announcementController import api as AnnouncementController

api = Api(title='My API')

api.add_namespace(user_controller, path='/user')
api.add_namespace(default_controller,path="/default")
api.add_namespace(kanban_controller, path="/kanban")
api.add_namespace(calendar_controller,path = "/calendar")
api.add_namespace(project_controller, path = "/project")
api.add_namespace(TeamMemberController, path = "/teammember")
api.add_namespace(AnnouncementController,path ="/announcement")