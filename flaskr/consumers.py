from kafka import KafkaConsumer
import json

consumer_user = KafkaConsumer(
    'user',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def consume_user(app):
    if app.config.get('MASTER_SLAVE_RELATION') == 'slave':
        for message in consumer_user:
            print(f"---------------message: {message.value}")