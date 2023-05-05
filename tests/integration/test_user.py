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
        """GIVEN no users WHEN adding new user THEN returns appropriate message."""

        payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        assert response.status_code == 201
        assert response.json['message'] == 'New user created.'

    def test_create_user_without_username(self):
        """GIVEN no users WHEN adding new user without username THEN service is denied."""
        payload = json.dumps({
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        assert response.status_code == 500
        assert response.json['message'] == 'Invalid information.'

    def test_create_user_without_password(self):
        """GIVEN no users WHEN adding new user without password THEN service is denied."""

        payload = json.dumps({
            "username": "test_user",
            "email": "test3@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        assert response.status_code == 500
        assert response.json['message'] == 'Invalid information.'

    def test_create_user_with_same_username(self):
        """GIVEN users WHEN adding new user with repeated username THEN service is denied."""

        payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        second_payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test2@email.com"
        })

        second_response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        assert second_response.status_code == 500
        assert second_response.json['message'] == "Username or email already exist."

    def test_create_user_with_same_email(self):
        """GIVEN users WHEN adding new user with repeated email THEN service is denied."""

        payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        second_payload = json.dumps({
            "username": "test_user2",
            "password": "password",
            "email": "test@email.com"
        })

        second_response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        assert second_response.status_code == 500
        assert second_response.json['message'] == "Username or email already exist."

    def test_get_user_by_public_id(self):
        """GIVEN users WHEN getting user by public_id THEN returns user details."""

        payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)
        public_id = response.json['public_id']

        get_response = self.client.get(f"{self.ROOT_URI}/user/{public_id}", headers=headers)

        assert get_response.status_code == 200
        assert get_response.json['user']['username'] == "test_user"

    def test_get_nonexistent_user_by_id(self):
        """GIVEN no users WHEN getting user by id THEN service is denied."""

        headers = {'Content-Type': 'application/json'}

        response = self.client.get(f"{self.ROOT_URI}/user/1234-567-890001", headers=headers)

        assert response.status_code == 404
        assert response.json['message'] == 'User not found.'
