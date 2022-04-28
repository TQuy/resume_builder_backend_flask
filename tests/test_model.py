import pytest
from sqlalchemy.exc import IntegrityError
from flaskr.models import *


def test_user_unique(app):
    with pytest.raises(IntegrityError) as excinfo:
        with app.app_context():
            a = User(username='a', password='a')
            db.session.add(a)
            db.session.commit()
            b = User(username='a', password='b')
            db.session.add(b)
            db.session.commit()
    assert "UNIQUE" in str(excinfo.value)
