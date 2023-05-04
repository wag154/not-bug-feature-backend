import json
from flask_testing import TestCase
from applications import create_app


class TestAuth(TestCase):
    ROOT_URI = "http://127.0.0.1:8000"

    def create_app(self):
        return create_app('TEST')

    def test_user_root(self):
        response = self.client.get(f"{self.ROOT_URI}/user/")
        assert response.status_code == 200
        assert response.json == 'hello'

    def test_create_user(self):
        payload = json.dumps({
            "username": "test_user_3",
            "password": "password",
            "email": "test3@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        assert response.status_code == 201
        assert response.json['message'] == 'New user created.'
