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
    resp = app.test_client().post("/project",json)
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
        "name": "hello world"
    })