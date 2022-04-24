from . import create_app
from .models import db


def drop_db():
    """
        Drop all tables in sqlite database
    """
    app = create_app()
    with app.app_context():
        db.drop_all()


if __name__ == "__main__":
    drop_db()
