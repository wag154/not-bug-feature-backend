from applications import app
import pytest


# GIVEN no users WHEN adding new user THEN returns new user.
def create_user():
    json = {
        "username": "test_user",
        "password": "password",
        "email": "test@email.com"
    }

    response = app.test_client().post('/register', json)
    data = response.data.decode('utf-8')

    assert response.status_code == 201
    assert data.username == "test_user"
    assert data.password == "password"
    assert data.email == "test@email.com"


# GIVEN no users WHEN adding new user without username THEN service is denied.
def create_user_no_username():
    json = {
        "password": "password",
        "email": "test@email.com"
    }

    response = app.test_client().post('/register', json)
    data = response.data.decode('utf-8')

    assert response.status_code == 502
    # TODO 1: assert data == some error


# GIVEN no users WHEN adding new user without password THEN service is denied.
def create_user_no_password():
    json = {
        "username": "test_user",
        "email": "test@email.com"
    }

    response = app.test_client().post('/register', json)
    data = response.data.decode('utf-8')

    assert response.status_code == 502
    # TODO 2: assert data == some error


# GIVEN users WHEN adding new user with repeated username THEN service is denied.
def create_user_repeated_username():
    json = {
        "username": "test_user",
        "password": "password",
        "email": "test@email.com"
    }

    response = app.test_client().post('/register', json)

    assert response.status_code == 201

    new_user_json = {
        "username": "test_user",
        "password": "password",
        "email": "test2@email.com"
    }

    new_response = app.test_client().post('/register', new_user_json)
    data = new_response.data.decode('utf-8')

    assert new_response.status_code == 502
    # TODO 3: assert data == some error


# GIVEN users WHEN adding new user with repeated email THEN service is denied.
def create_user_repeated_email():
    json = {
        "username": "test_user",
        "password": "password",
        "email": "test@email.com"
    }

    response = app.test_client().post('/register', json)

    assert response.status_code == 201

    new_user_json = {
        "username": "test_user2",
        "password": "password",
        "email": "test@email.com"
    }

    new_response = app.test_client().post('/register', new_user_json)
    data = new_response.data.decode('utf-8')

    assert new_response.status_code == 502
    # TODO 4: assert data == some error


# GIVEN users WHEN getting user by id THEN returns user.
def get_user_by_id():
    json = {
        "username": "test_user",
        "password": "password",
        "email": "test@email.com"
    }

    response = app.test_client().post('/register', json)

    assert response.status_code == 201

    user_by_id_response = app.test_client().get('/user/1')
    data = user_by_id_response.data.decode('utf-8')

    assert user_by_id_response.status_code == 200
    assert data.username == "test_user"
    assert data.password == "password"
    assert data.email == "test@email.com"


# GIVEN no users WHEN getting user by id THEN service is denied.
def get_user_by_unexisting_id():
    response = app.test_client().get('/user/999999')
    data = response.data.decode('utf-8')

    assert response.status_code == 502
    # TODO 5: assert data == some error