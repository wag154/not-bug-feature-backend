from applications import app
import pytest
import requests
import json

@pytest.fixture()
def test_app():
    app.config.update({
        "TESTING" : True,
    })
    return app.test_client()

def test_default():
    resp = app.test_client().get('/')
    assert resp.status_code == 200
    assert resp.data.decode('utf-8') == 'hello'

def test_increase_level():
    resp = app.test_cl.post('/add',json={
        "name": "hallo"
    })
    data = resp.data.decode('utf-8')
    
def test_create_project ():
    resp = app.test_client().post("/project",json={
        "user_id"  : "1",
        "title" : "best project",
        "description" : "unequaled on earth!",
        "duration" : "7",
        "tech_stack" : "yes",
        "position" : "frontend,backend"
    })
    assert resp.status_code == 200

def test_get_project():
    resp = app.test_client().get("/project/1")
    data = resp.data.decode('utf-8')
    assert data["name"]
    assert resp.status_code == 200

def test_update_project():
    resp = app.test_client().put("/project/1")
    data = resp.data.decode('utf-8')
    assert resp.status_code == 200

def test_delete_project():
    resp = app.test_client().put("/project")
    #data = resp.data.decode('utf-8')
    assert resp.status_code == 200

def test_get_project_by_user(): 
    resp = app.test_client().get("/projectbyuser/1")
    data = resp.data.decode('utf-8')
    assert resp.status_code == 200
    assert data["name"]

def test_create_kanban():
    resp = app.test_client().post("/kanban/1",json={
        "name":"Test",
        "category" : "hello world,goodbye world" 
    })
    assert resp.status_code == 200

def test_create_kanban_task ():
    resp = app.test_client().post("/kanban/1&1",{
        "name": "hello world",
        "objective" :"print('hello world')",
        "category" : "hello world"
    })
    assert resp.status_code == 200

def test_get_all_kanban_tasks():
    resp  = app.test_client().get("/kanban/1")

    assert len(resp.data.decode('utf-8')) != 0
    assert resp.status_code == 200

def test_delete_kanban_tasks():
    resp = app.test_client().delete("/kanban/1&1")
    assert resp.status_code == 200

def test_update_kanban_task():
    resp = app.test_client().put("/kanban/1&1",json={
        "name" : "World Hello",
        "objective" : "print('world hello')",
        "category" : "hello world"
    })
    assert resp.status_code == 200
def test_edit_kanban ():
    resp = app.test_client.put("/kanban/1",json={
        "name" : "Yes",
        "Category" : "goodbye world,hello world"
    })
    assert resp.status_code == 200

def test_remove_kanban():
    resp = app.test_client.delete("/kanban/1")
    assert resp.status_code == 200

def test_get_calendar():
    resp = app.test_client.get("/calendar/1")
    assert resp.status_code == 200 

def test_create_calendar():
    resp = app.test_client.post("/calendar/1",json={
        "name" : "test",
        "duration" : "7"
    })
    assert resp.status_code == 200

def test_calendar_card_create():
    resp = app.test_client.post("/calendar/1",json = {
        "name" : "Defeat the ender dragon",
        "DueDate": "11/05/2023"
    })
    assert resp.status_code == 200

def test_calendar_card_change():
    resp = app.test_client.put("/calendar/1",json ={
        "name" : "Defeat the ender dragon",
        "DueDate" : "12/05/2023"
    })
    assert resp.status_code == 200

def test_project_member_created():
    resp = app.test_client.post("/projectmember/1&1",json ={
        "level" : "2",
        "role" : "1"
    })
    assert resp.status_code == 200

    resp2 = app.test_client.post("/projectmember/1&1",json ={
        "levela" : "2",
        "role" : "1"
    })
    assert resp2.status_code == 404

def test_member_edit():
    resp = app.test_client.put("/projectmember/1&1",json={
        "level" = "2",
        "role" = "2"
    })
    assert resp.status_code == 200
    

def test_member_remove():
    resp = app.test_client.delete("/projectmember/1&1")
    assert resp.status_code == 200

