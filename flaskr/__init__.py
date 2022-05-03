import os

from flask import Flask
from flask_cors import CORS
from flaskr.models import db, migrate
from flaskr.api import auth, resume
from flaskr import signals
from flaskr.consumers import consume_user


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'sqlalchemy_tutorial.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        MASTER_SLAVE_RELATION="master",
        SLAVE_HOST="http://localhost:4000/",
        KAFKA_HOST="localhost:9092",
    )
    CORS(app, origins=["http://localhost:3000"])

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello/')
    def hello():
        return 'Hello, World!'

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(auth.bp)
    app.register_blueprint(resume.bp)
    consume_user(app)

    return app
