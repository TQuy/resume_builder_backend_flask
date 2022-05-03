import json
from kafka import KafkaProducer
from datetime import datetime
from time import sleep

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x:json.dumps({
        'timestamp':x
    }).encode('utf-8')
)

while True:
    timestampEvent = datetime.now().strftime("%H:%M:%S")
    print("Sending: " + timestampEvent)
    future = producer.send('timestamp', timestampEvent)
    print(f"-----------future: {future.__dict__}")
    sleep(5)