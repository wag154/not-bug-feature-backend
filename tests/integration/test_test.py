import json
from flask_testing import TestCase
from applications import create_app, db
import base64


class TestAuth(TestCase):
    ROOT_URI = "http://127.0.0.1:8000"

    def create_app(self):
        return create_app('TEST')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_default(self):
        resp = self.client.get(f"/")
        assert resp.status_code == 200

    # def test_increase_level(self):
    #     payload = {
    #         "name": "hallo"
    #     }
    #     resp = self.client.post('/add', payload)
    #     data = resp.data.decode('utf-8')
#
    def test_create_project(self):
        """GIVEN no projects WHEN trying to create new project THEN returns 201."""
        payload = json.dumps({
            "title": "best project",
            "description": "unequaled on earth!",
            "tech_stack": "yes",
            "positions": "frontend,backend",
            "user_id": "1",
            "duration": "7",
            "chatroom_key": "this-will-be-a-chatroom-key",
            "number_of_collaborators": "0"
        })

        headers = {'Content-Type': 'application/json'}

        resp = self.client.post(f"{self.ROOT_URI}/project/1", data=payload, headers=headers)
        assert resp.status_code == 201

    def test_get_project(self):
        """GIVEN project WHEN trying to get project information THEN information is returned."""

        # Creating project.
        payload = json.dumps({
            "title": "best project",
            "description": "unequaled on earth!",
            "tech_stack": "yes",
            "positions": "frontend,backend",
            "user_id": "1",
            "duration": "7",
            "chatroom_key": "this-will-be-a-chatroom-key",
            "number_of_collaborators": "0"
        })

        headers = {'Content-Type': 'application/json'}

        resp = self.client.post(f"{self.ROOT_URI}/project/1", data=payload, headers=headers)
        assert resp.status_code == 201

        # Getting project information.
        get_resp = self.client.get(f"{self.ROOT_URI}/project/1")
        assert get_resp.json['user projects'][0]['title'] == 'best project'
        assert get_resp.status_code == 200

    def test_update_project(self):
        """GIVEN user and project WHEN trying to update project details THEN returns message and 200."""
        # Creating a user.
        user_payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=user_payload, headers=headers)

        assert response.status_code == 201
        assert response.json['message'] == 'New user created.'

        # Creating project.
        payload = json.dumps({
            "title": "best project",
            "description": "unequaled on earth!",
            "tech_stack": "yes",
            "positions": "frontend,backend",
            "user_id": "1",
            "duration": "7",
            "chatroom_key": "this-will-be-a-chatroom-key",
            "number_of_collaborators": "0"
        })

        resp = self.client.post(f"{self.ROOT_URI}/project/1", data=payload, headers=headers)
        assert resp.status_code == 201

        # Updating project.
        put_payload = json.dumps({
            "title": "new project title",
            "description": "this is a description",
            "tech_stack": "tech stack list",
            "positions": "1",
            "user_id": "1",
            "duration": "1",
            "number_of_collaborators": "1"
        })
        put_resp = self.client.put(f"{self.ROOT_URI}/project/1", data=put_payload, headers=headers)
        assert put_resp.status_code == 200
        assert put_resp.json['Message'] == 'Success!'

    def test_delete_project(self):
        """GIVEN project and user WHEN deleting project THEN message is returned."""
        # Creating a user.
        user_payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=user_payload, headers=headers)

        assert response.status_code == 201
        assert response.json['message'] == 'New user created.'

        # Creating project.
        payload = json.dumps({
            "title": "best project",
            "description": "unequaled on earth!",
            "tech_stack": "yes",
            "positions": "frontend,backend",
            "user_id": "1",
            "duration": "7",
            "chatroom_key": "this-will-be-a-chatroom-key",
            "number_of_collaborators": "0"
        })

        resp = self.client.post(f"{self.ROOT_URI}/project/1", data=payload, headers=headers)
        assert resp.status_code == 201

        # Deleting project.
        delete_resp = self.client.delete(f"{self.ROOT_URI}/project/1", headers=headers)
        assert delete_resp.json['Message'] == 'success'
        assert delete_resp.status_code == 200

    def test_get_project_by_user(self):
        """GIVEN project and user WHEN getting project by user id THEN """
        # Creating a user.
        user_payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=user_payload, headers=headers)

        assert response.status_code == 201
        assert response.json['message'] == 'New user created.'

        # Creating project.
        payload = json.dumps({
            "title": "best project",
            "description": "unequaled on earth!",
            "tech_stack": "yes",
            "positions": "frontend,backend",
            "user_id": "1",
            "duration": "7",
            "chatroom_key": "this-will-be-a-chatroom-key",
            "number_of_collaborators": "0"
        })

        resp = self.client.post(f"{self.ROOT_URI}/project/1", data=payload, headers=headers)
        assert resp.status_code == 201

        # Getting project info.
        resp = self.client.get(f"{self.ROOT_URI}/project/1")
        assert resp.status_code == 200
        assert resp.json["user projects"][0]['title'] == 'best project'

    def test_create_kanban(self):
        """GIVEN user and project WHEN kanban is created THEN returns 200."""
        # Creating a user.
        user_payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=user_payload, headers=headers)

        assert response.status_code == 201
        assert response.json['message'] == 'New user created.'

        # Creating project.
        payload = json.dumps({
            "title": "best project",
            "description": "unequaled on earth!",
            "tech_stack": "yes",
            "positions": "frontend,backend",
            "user_id": "1",
            "duration": "7",
            "chatroom_key": "this-will-be-a-chatroom-key",
            "number_of_collaborators": "0"
        })

        # Creating kanban board.
        kanban_payload = {
            "name": "Test",
            "category": "hello world,goodbye world"
        }

        resp = self.client.post(f"{self.ROOT_URI}/kanban/1", data=kanban_payload, headers=headers)
        assert resp.status_code == 200

    def test_create_kanban_task (self):
        """GIVEN user, project and kanban WHEN creating new task THEN returns 200."""
        # Creating a user.
        user_payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=user_payload, headers=headers)

        assert response.status_code == 201
        assert response.json['message'] == 'New user created.'

        # Creating project.
        payload = json.dumps({
            "title": "best project",
            "description": "unequaled on earth!",
            "tech_stack": "yes",
            "positions": "frontend,backend",
            "user_id": "1",
            "duration": "7",
            "chatroom_key": "this-will-be-a-chatroom-key",
            "number_of_collaborators": "0"
        })

        # Creating kanban board.
        kanban_payload = {
            "name": "Test",
            "category": "hello world,goodbye world"
        }

        resp = self.client.post(f"{self.ROOT_URI}/kanban/1", data=kanban_payload, headers=headers)
        assert resp.status_code == 200

        # Adding task to kanban board.
        task_payload = {
            "name": "hello world",
            "objective" :"print('hello world')",
            "category" : "hello world"
        }
        resp2 = self.client.post("/kanban/task/1", data=task_payload, headers=headers)
        assert resp.status_code == 200
#
    def test_get_all_kanban_tasks(self):
        """GIVEN user, project, kanban board and task WHEN retrieving all tasks THEN return 200."""
        # Creating a user.
        user_payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=user_payload, headers=headers)

        assert response.status_code == 201
        assert response.json['message'] == 'New user created.'

        # Creating project.
        payload = json.dumps({
            "title": "best project",
            "description": "unequaled on earth!",
            "tech_stack": "yes",
            "positions": "frontend,backend",
            "user_id": "1",
            "duration": "7",
            "chatroom_key": "this-will-be-a-chatroom-key",
            "number_of_collaborators": "0"
        })

        # Creating kanban board.
        kanban_payload = {
            "name": "Test",
            "category": "hello world,goodbye world"
        }

        resp = self.client.post(f"{self.ROOT_URI}/kanban/1", data=kanban_payload, headers=headers)
        assert resp.status_code == 200

        # Adding task to kanban board.
        task_payload = {
            "name": "hello world",
            "objective": "print('hello world')",
            "category": "hello world"
        }
        resp2 = self.client.post("/kanban/task/1", data=task_payload, headers=headers)
        assert resp.status_code == 200

        # Getting kanban tasks.
        resp3 = self.client.get(f"{self.ROOT_URI}/kanban/task/1")

        assert len(resp3.json["All tasks"]) != 0
        assert resp.status_code == 200

    # TODO: check if test below is correct.
    def test_delete_kanban_tasks(self):
        """GIVEN user, project, kanban board and task WHEN deleting a task THEN returns 200."""
        # Creating a user.
        user_payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=user_payload, headers=headers)

        assert response.status_code == 201
        assert response.json['message'] == 'New user created.'

        # Creating project.
        payload = json.dumps({
            "title": "best project",
            "description": "unequaled on earth!",
            "tech_stack": "yes",
            "positions": "frontend,backend",
            "user_id": "1",
            "duration": "7",
            "chatroom_key": "this-will-be-a-chatroom-key",
            "number_of_collaborators": "0"
        })

        # Creating kanban board.
        kanban_payload = {
            "name": "Test",
            "category": "hello world,goodbye world"
        }

        resp = self.client.post(f"{self.ROOT_URI}/kanban/1", data=kanban_payload, headers=headers)
        assert resp.status_code == 200

        # Adding task to kanban board.
        task_payload = {
            "name": "hello world",
            "objective": "print('hello world')",
            "category": "hello world"
        }
        resp2 = self.client.post("/kanban/task/1", data=task_payload, headers=headers)
        assert resp.status_code == 200

        # Deleting task.
        resp3 = self.client.delete(f"{self.ROOT_URI}/kanban/task/1")
        assert resp3.status_code == 200

    def test_update_kanban_task(self):
        """GIVEN user, project, kanban board and task WHEN updating task THEN returns 200."""
        # Creating a user.
        user_payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=user_payload, headers=headers)

        assert response.status_code == 201
        assert response.json['message'] == 'New user created.'

        # Creating project.
        payload = json.dumps({
            "title": "best project",
            "description": "unequaled on earth!",
            "tech_stack": "yes",
            "positions": "frontend,backend",
            "user_id": "1",
            "duration": "7",
            "chatroom_key": "this-will-be-a-chatroom-key",
            "number_of_collaborators": "0"
        })

        # Creating kanban board.
        kanban_payload = {
            "name": "Test",
            "category": "hello world,goodbye world"
        }

        resp = self.client.post(f"{self.ROOT_URI}/kanban/1", data=kanban_payload, headers=headers)
        assert resp.status_code == 200

        # Adding task to kanban board.
        task_payload = json.dumps({
            "name": "hello world",
            "objective": "print('hello world')",
            "category": "hello world"
        })
        resp2 = self.client.post("/kanban/task/1", data=task_payload, headers=headers)
        assert resp.status_code == 200

        # Updating task.
        put_payload = json.dumps({
            "name" : "World Hello",
            "objective" : "print('world hello')",
            "category" : "hello world"
        })

        resp3 = self.client.put("/kanban/task/1", data=put_payload, headers=headers)
        assert resp3.status_code == 200

    def test_edit_kanban (self):
        """GIVEN user, project and kanban WHEN updating kanban THEN returns 200."""

        # Creating a user.
        user_payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=user_payload, headers=headers)

        assert response.status_code == 201
        assert response.json['message'] == 'New user created.'

        # Creating project.
        payload = json.dumps({
            "title": "best project",
            "description": "unequaled on earth!",
            "tech_stack": "yes",
            "positions": "frontend,backend",
            "user_id": "1",
            "duration": "7",
            "chatroom_key": "this-will-be-a-chatroom-key",
            "number_of_collaborators": "0"
        })

        # Creating kanban board.
        kanban_payload = {
            "name": "Test",
            "category": "hello world,goodbye world"
        }

        resp = self.client.post(f"{self.ROOT_URI}/kanban/1", data=kanban_payload, headers=headers)
        assert resp.status_code == 200

        # Updating kanban board.
        put_payload = json.dumps({
            "name": "Yes",
            "categories": "goodbye world,hello world"
        })
        resp2 = self.client.put(f"{self.ROOT_URI}/kanban/1", data=put_payload, headers=headers)
        assert resp2.status_code == 200
#
# def test_remove_kanban():
#     resp = app.test_client.delete("/kanban/1")
#     assert resp.status_code == 200
#
# def test_get_calendar():
#     resp = app.test_client.get("/calendar/1")
#     assert resp.status_code == 200
#
# def test_create_calendar():
#     resp = app.test_client.post("/calendar/1",json={
#         "name" : "test",
#         "duration" : "7"
#     })
#     assert resp.status_code == 200
#
# def test_calendar_card_create():
#     resp = app.test_client.post("/calendar/1",json = {
#         "name" : "Defeat the ender dragon",
#         "DueDate": "11/05/2023"
#     })
#     assert resp.status_code == 200
#
# def test_calendar_card_change():
#     resp = app.test_client.put("/calendar/1",json ={
#         "name" : "Defeat the ender dragon",
#         "DueDate" : "12/05/2023"
#     })
#     assert resp.status_code == 200
#
# def test_project_member_created():
#     resp = app.test_client.post("/projectmember/1&1",json ={
#         "level" : "2",
#         "role" : "1"
#     })
#     assert resp.status_code == 200
#
#     resp2 = app.test_client.post("/projectmember/1&1",json ={
#         "levela" : "2",
#         "role" : "1"
#     })
#     assert resp2.status_code == 404
#
# def test_member_edit():
#     resp = app.test_client.put("/projectmember/1&1",json={
#         "level" = "2",
#         "role" = "2"
#     })
#     assert resp.status_code == 200
#
#
# def test_member_remove():
#     resp = app.test_client.delete("/projectmember/1&1")
#     assert resp.status_code == 200
#
# # from applications import app
# # import pytest
# # def test_default():
# #     resp = app.test_client().get('/')
# #     assert resp.status_code == 200
# #     assert resp.data.decode('utf-8') == 'hello'
# #
# # # def test_increase_level():
# # #     resp = app.