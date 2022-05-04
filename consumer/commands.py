from token import tok_name
import click
from kafka import KafkaConsumer
import json
import requests
from flask.cli import with_appcontext
from config import ConsumerConfig

@click.command('async-user')
@with_appcontext
def async_user():
    user_consumer = KafkaConsumer(
        'user',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in user_consumer:
        print(f"-------------------message: {message.value}")

        response = requests.post(
            f"{ConsumerConfig.SLAVE_HOST}auth/register/",
            json = message.value
        )
        print(f"response: {response.__dict__}")

    # assert response.status_code == 2