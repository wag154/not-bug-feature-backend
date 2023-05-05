from applications import create_app
from flask_testing import TestCase
import json

class TestProject(TestCase):
    ROOT_URI = "http://127.0.0.1:8000"

    def create_app(self):
        return create_app("TEST") 
    def setUp(self):
        self.client.post("/user",json={
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
    def test_create_project(self):
        resp = self.client.post("/project/1", json={
            "user_id" : "1",
            "title" : "best project",
            "description" : "unequaled on earth!",
            "number_of_collaborators" : "3",
            "duration" : "7",
            "tech_stack" : "yes",
            "chatroom_key" : "123"
            "positions" : "frontend,backend"
        })
        assert resp.status_code == 201

    #def test_get_project(self):
      #  resp = self.client.get("/project/1")
    #    data = (resp.data)
     #   check = data.get("name")
     #   assert check
     #   assert resp.status_code == 200

    def test_update_project(self):
        resp = self.client.put("/project/1", json={
            "title": "new title",
            "description": "new description",
            "duration": "14"
        })
        assert resp.status_code == 200

    def test_delete_project(self):
        resp = self.client.delete("/project/1")
        assert resp.status_code == 200
        

