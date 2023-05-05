from applications import create_app
from applications.database import db
from unittest import TestCase
import json

class TestKanban(TestCase):
    ROOT_URI = "http://127.0.0.1:8000"
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    def test_create_kanban(self):
        resp = self.client.post("/kanban/1",json={
         "name":"Test",
        "categories":"hello world,goodbye world" 
        })
        assert resp.status_code == 200

    def test_create_kanban_task (self):
        #response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)
        payload = json.dumps({
            "name": "hello world",
          "objective" :"print('hello world')",
          "category" : "hello world"
        })
        headers = {'Content-Type': 'application/json'}
        resp = self.client.post(f"{self.ROOT_URI}/kanban/task/1", headers= headers,data = payload)
        print(resp.json)
        assert resp.status_code == 200

   # def test_get_all_kanban_tasks(self):
     #   resp  = self.client.get("/kanban/task/1")
      #  assert resp.status_code == 200

   # def test_update_kanban_task(self):
       # resp = self.client.put("/kanban/task/1",json={
       #     "name" : "World Hello",
       #     "objective" : "print('world hello')",
       #     "category" : "hello world"
    #     })
       # assert resp.status_code == 200

    #def test_edit_kanban (self):
       # resp = self.client.put("/kanban/1",json={
      #      "name" : "Yes",
      #      "categories" : "goodbye world,hello world"
      #})
     #   assert resp.status_code == 200
    