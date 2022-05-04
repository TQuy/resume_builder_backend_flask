from kafka import KafkaConsumer
import json

consumer_user = KafkaConsumer(
    'timestamp',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# for message in consumer_user:
#     print(f"---------------message: {message.value}")
