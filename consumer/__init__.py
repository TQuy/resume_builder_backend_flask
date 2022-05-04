from flask import Flask
from consumer.commands import async_user

def create_app():
    app = Flask(__name__)
    app.cli.add_command(async_user)
    return app
