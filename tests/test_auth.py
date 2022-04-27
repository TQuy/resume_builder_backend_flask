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

    response = client.post(
        '/auth/register/', json={'username': 'a', 'password': 'a', 'confirm_password': 'a'}
    )
    assert response.status_code == 400

    message = json.loads(response.data)['message']
    assert message == f"User {username} is already registered."

# def test_login(client, app):
