from flaskr.models import User, Resume, db
from flaskr.services.auth import generate_jwt_token
from sqlalchemy import event
import requests

slave_host = "http://localhost:4000/"


@event.listens_for(User, 'after_insert')
def sync_user(mapper, connection, target):
    response = requests.post(f"{slave_host}auth/register/", json={
        'username': target.username,
        'password': target.password,
        'confirm_password': target.password,
    })
    assert response.status_code == 201


@event.listens_for(Resume, 'after_insert')
@event.listens_for(Resume, 'after_update')
def sync_saved_resume(mapper, connection, target):
    token = get_token_from_resume(target)
    response = requests.post(
        f"{slave_host}resume/save/",
        headers={
            'Authorization': token,
        },
        json={
            'name': target.name,
            'content': target.content,
            'user_id': target.user_id,
        },
    )
    assert response.status_code == 200


@event.listens_for(Resume, 'after_delete')
def sync_deleted_resume(mapper, connection, target):
    token = get_token_from_resume(target)
    response = requests.delete(
        f"{slave_host}resume/save/{target.id}",
        headers={
            'Authorization': token,
        }
    )
    assert response.status_code == 200


def get_token_from_resume(resume) -> str:
    current_user = User.query.filter_by(id=resume.user_id)
    token = generate_jwt_token(current_user)
    return token
