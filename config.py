import os


class DevConfig():
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'instance', 'sqlalchemy_tutorial.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    MASTER_SLAVE_RELATION = "master"
    # MASTER_SLAVE_RELATION = "slave"
    SLAVE_HOST = "http://localhost:4000/"
    KAFKA_HOST = "localhost:9092"

class ConsumerConfig():
    SLAVE_HOST = 'http://localhost:4000/'