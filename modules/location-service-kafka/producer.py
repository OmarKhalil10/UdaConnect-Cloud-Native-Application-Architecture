import os
import json
from kafka import KafkaProducer

# Choose one topic name; here we match "locations" for both producer and consumer
TOPIC_NAME = os.environ.get("TOPIC_NAME", "locations")
KAFKA_SERVER = os.environ.get("KAFKA_SERVER", "localhost:9092")

# Producer that serializes Python dict to JSON bytes
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Sample message data
message_data = {
    "person_id": 123,
    "longitude": "-73.935242",
    "latitude": "40.73061"
}

print(f"[PRODUCER] Sending to topic='{TOPIC_NAME}' on broker='{KAFKA_SERVER}'")
# Send the message asynchronously
future = producer.send(TOPIC_NAME, message_data)
producer.flush()

try:
    record_metadata = future.get(timeout=10)
    print(f"[PRODUCER] Message delivered to partition {record_metadata.partition}, offset {record_metadata.offset}")
except Exception as e:
    print(f"[PRODUCER] Failed to send message: {e}")
