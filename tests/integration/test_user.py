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
            "email": "test@email.com"
        })

        second_response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        assert second_response.status_code == 500
        assert second_response.json['message'] == "Username or email already exist."

    def test_create_user_with_same_email(self):
        """GIVEN users WHEN adding new user with repeated email THEN service is denied."""

        payload = json.dumps({
            "username": "test_user2",
            "password": "password",
            "email": "test2@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        second_payload = json.dumps({
            "username": "test_user3",
            "password": "password",
            "email": "test2@email.com"
        })

        second_response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        assert second_response.status_code == 500
        assert second_response.json['message'] == "Username or email already exist."

    def test_get_user_by_username(self):
        """GIVEN users WHEN getting user by username THEN returns user details."""

        # Creating new user.
        payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        create_response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        # Loging in.
        valid_credentials = base64.b64encode(b"test_user:password").decode("utf-8")
        auth_header = {"Authorization": "Basic " + valid_credentials}
        login_response = self.client.get(f"{self.ROOT_URI}/user/login", headers=auth_header)
        token = login_response.json['token']

        # Getting user information.
        headers_with_token = {'Content-Type': 'application/json', 'x-access-token': token}

        get_response = self.client.get(f"{self.ROOT_URI}/user/test_user", headers=headers_with_token)

        assert get_response.status_code == 200
        assert get_response.json['user']['username'] == "test_user"

    def test_get_nonexistent_user_by_username(self):
        """GIVEN no users WHEN getting user by username THEN service is denied."""

        # Creating new user.
        payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        create_response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)

        # Loging in.
        valid_credentials = base64.b64encode(b"test_user:password").decode("utf-8")
        auth_header = {"Authorization": "Basic " + valid_credentials}
        login_response = self.client.get(f"{self.ROOT_URI}/user/login", headers=auth_header)
        token = login_response.json['token']

        # Getting user information.
        headers_with_token = {'Content-Type': 'application/json', 'x-access-token': token}

        get_response = self.client.get(f"{self.ROOT_URI}/user/wrong_user", headers=headers_with_token)

        assert get_response.status_code == 404
        assert get_response.json['message'] == 'User not found.'

    def test_updating_user_details(self):
        # Creating new user.
        payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        create_response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)
        assert create_response.status_code == 201
        #
        # Loging in.
        valid_credentials = base64.b64encode(b"test_user:password").decode("utf-8")
        auth_header = {"Authorization": "Basic " + valid_credentials}
        login_response = self.client.get(f"{self.ROOT_URI}/user/login", headers=auth_header)
        assert login_response.status_code == 200
        token = login_response.json['token']

        # Updating details.
        token_header = {'x-access-token': token, 'Content-Type': 'application/json'}
        update_payload = json.dumps({
            "name": "test user name",
            "skill_level": "skill level",
            "skills": "a list of skills",
            "role": "role"
        })
        update_response = self.client.patch(f"{self.ROOT_URI}/user/test_user", headers=token_header, data=update_payload)
        print('HERE', update_response)
        assert update_response.status_code == 202
        assert update_response.json['message'] == 'User details successfully updated.'

    def test_login_with_no_credentials(self):
        """GIVEN no credentials are passed WHEN logging  in THEN returns 401."""
        # Creating new user.
        payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        create_response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)
        assert create_response.status_code == 201

        # Loging in.
        invalid_credentials = base64.b64encode(b" : ").decode("utf-8")
        auth_header = {"Authorization": "Basic " + invalid_credentials}
        login_response = self.client.get(f"{self.ROOT_URI}/user/login", headers=auth_header)
        assert login_response.status_code == 401

    def test_login_with_invalid_username(self):
        """GIVEN invalid username WHEN logging  in THEN returns 401."""
        # Loging in.
        valid_credentials = base64.b64encode(b"test_user:password").decode("utf-8")
        auth_header = {"Authorization": "Basic " + valid_credentials}
        login_response = self.client.get(f"{self.ROOT_URI}/user/login", headers=auth_header)
        assert login_response.status_code == 401

    def test_login(self):
        """GIVEN correct credentials WHEN logging in THEN returns proper message."""
        # Creating new user.
        payload = json.dumps({
            "username": "test_user",
            "password": "password",
            "email": "test@email.com"
        })
        headers = {'Content-Type': 'application/json'}

        create_response = self.client.post(f"{self.ROOT_URI}/user/", data=payload, headers=headers)
        assert create_response.status_code == 201
        #
        # Loging in.
        valid_credentials = base64.b64encode(b"test_user:password").decode("utf-8")
        auth_header = {"Authorization": "Basic " + valid_credentials}
        login_response = self.client.get(f"{self.ROOT_URI}/user/login", headers=auth_header)
        assert login_response.status_code == 200
        assert login_response.json['message'] == 'Access granted.'
