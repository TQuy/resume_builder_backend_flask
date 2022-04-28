import json
import pytest
from flaskr.models import *
from sqlalchemy import select


def test_register(client, app):

    username = 'a'
    password = 'a'
    confirm_password = password
    response = client.post(
        '/auth/register/', json={'username': username, 'password': password, 'confirm_password': confirm_password}
    )
    assert response.status_code == 201

    with app.app_context():
        assert db.session.scalar(select(User).where(User.username == 'a'))


@pytest.mark.parametrize(('username', 'password', 'confirm_password', 'message'), (
    ('', '', '', 'Username is required.'),
    ('a', '', '', 'Password is required.'),
    ('a', 'a', '', 'The password and confirm password are not the same.')
))
def test_register_validate_input(
        client, username, password, confirm_password, message):
    response = client.post(
        '/auth/register/', json={'username': username, 'password': password, 'confirm_password': confirm_password}
    )
    assert message == json.loads(response.data).get('message')


def test_register_wrong_method(client):
    response = client.get('/auth/register/')
    assert response.status_code == 405


def test_login(client):
    user = AuthUser(client, username='a', password='a')
    token = user.login()
    assert isinstance(token, str)


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', 'Username is required.'),
    ('a', '', 'Password is required.'),
))
def test_login_validate_input(client, username, password, message):
    response = client.post(
        '/auth/login/',
        json={'username': username, 'password': password}
    )

    assert message == json.loads(response.data).get('message')


def test_login_wrong_method(client):
    response = client.get(
        '/auth/login/'
    )
    assert response.status_code == 405

# --------------------------------------------------------------------------


class AuthUser():
    def __init__(self, client, username, password):
        self._client = client
        self.username = username
        self.password = password
        self.register()

    def register(self):
        response = self._client.post(
            '/auth/register/', json={'username': self.username, 'password': self.password, 'confirm_password': self.password}
        )
        assert response.status_code == 201

    def login(self):
        response = self._client.post(
            '/auth/login/',
            json={'username': self.username, 'password': self.password}
        )

        assert response.status_code == 200

        return json.loads(response.data).get('token')
