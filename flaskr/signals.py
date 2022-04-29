from flaskr.models import User, Resume, db
from sqlalchemy import event


@event.listens_for(User, 'after_insert')
def sync_user(mapper, connection, target):
    print("---------------------------------------fsafsaf-----------------")
    print(f"------------------mapper: {mapper}, type: {type(mapper)}, dict: {mapper.__dict__}")
    print(f"------------------target: {target}, type: {type(target)}, dict: {target.__dict__}")