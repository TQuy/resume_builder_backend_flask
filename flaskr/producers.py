import json
from kafka import KafkaProducer
from datetime import datetime
from time import sleep
from flask import current_app


producer = KafkaProducer(
    bootstrap_servers=current_app.config.get('KAFKA_HOST'),
    # x is dictionary
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
)

# producer_saved_resume = KafkaProducer(
#     bootstrap_servers=current_app.config.get('KAFKA_HOST'),
#     value_serializer=lambda x: json.dumps(x).encode('utf-8'),
# )

# while True:
#     timestampEvent = datetime.now().strftime("%H:%M:%S")
#     print("Sending: " + timestampEvent)
#     producer.send('timestamp', timestampEvent)
#     sleep(5)
