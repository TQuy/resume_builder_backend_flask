import pytest
import json
from test_auth import AuthUser
from flaskr.models import *


def test_list_resume_not_authorized(client):
    response = client.get('/resume/list/')
    assert response.status_code == 200
    list_resume = json.loads(response.data).get('content', None)
    assert list_resume is None


def test_list_resume(client, app):
    auth_user = AuthUser(client, 'a', 'a')
    token = auth_user.login()
    assert isinstance(token, str)
    # call the request when there is no resume present.
    response = client.get('/resume/list/', headers={
        'Authorization': token
    })
    assert response.status_code == 200
    list_resume = json.loads(response.data).get('content', None)
    assert isinstance(list_resume, list)
    assert len(list_resume) == 0
    # insert one resume and list again
    with app.app_context():
        resume = Resume(
            name='a',
            content='hello',
            user=User.query.filter_by(
                username=auth_user.username).one())
        db.session.add(resume)
        db.session.commit()
        assert Resume.query.count() == 1
    response = client.get('/resume/list/', headers={
        'Authorization': token
    })
    list_resume = json.loads(response.data).get('content', None)
    assert len(list_resume) == 1
