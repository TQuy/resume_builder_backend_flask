from . import create_app
from .models import db

def init_db():
    """
        Init sqlite database
    """
    app = create_app()
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()