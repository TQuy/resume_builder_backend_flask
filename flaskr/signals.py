from flaskr.models import User, Resume
from flaskr.services.auth import generate_jwt_token
from sqlalchemy import event
from flask import current_app
from flaskr.producers import producer
from datetime import datetime
from time import sleep

@event.listens_for(User, 'after_insert')
def async_user(mapper, connection, target):
    print("-------------------------------------")
    if (current_app.config.get('MASTER_SLAVE_RELATION') == 'slave'):
        return
    # future = producer.send('user', {
    #     'username': target.username,
    #     'password': target.password,
    #     'confirm_password': target.password,
    # })
    timestampEvent = datetime.now().strftime("%H:%M:%S")
    print("Sending: " + timestampEvent)
    future = producer.send('timestamp', timestampEvent)
    sleep(5)
    assert future.is_done is True


@event.listens_for(Resume, 'after_insert')
@event.listens_for(Resume, 'after_update')
def async_saved_resume(mapper, connection, target):
    if (current_app.config.get('MASTER_SLAVE_RELATION') == 'slave'):
        return
    token = get_token_from_resume(target)
    future = producer.send('updated_resume', {
        'Authorization': token,
        'name': target.name,
        'content': target.content,
        'user_id': target.user_id,
    })
    assert future.is_done is True


@event.listens_for(Resume, 'after_delete')
def async_deleted_resume(mapper, connection, target):
    if (current_app.config.get('MASTER_SLAVE_RELATION') == 'slave'):
        return
    token = get_token_from_resume(target)
    future = producer.send('updated_resume', {
        'Authorization': token,
    })
    assert future.is_done is True


def get_token_from_resume(resume) -> str:
    if (current_app.config.get('MASTER_SLAVE_RELATION') == 'slave'):
        return
    current_user = User.query.filter_by(id=resume.user_id).one()
    token = generate_jwt_token(current_user)
    return token
