import os
import json
import psycopg2
from datetime import datetime
from kafka import KafkaConsumer

# Environment variables (typically set in a deployment or shell)
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
TOPIC_NAME = os.environ.get("TOPIC_NAME", "locations")
KAFKA_SERVER = os.environ.get("KAFKA_SERVER", "localhost:9092")

# Subscribe to the same topic the producer uses
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

print(f"[CONSUMER] Listening on topic '{TOPIC_NAME}' at {KAFKA_SERVER}...")

for message in consumer:
    # Decode bytes → string → JSON dict
    decoded_kafka_message = message.value.decode("utf-8")
    location_dict = json.loads(decoded_kafka_message)

    print("[CONSUMER] Received:", location_dict)
    # e.g. {"person_id": 123, "longitude": "-73.935242", "latitude": "40.73061"}

    # Connect to Postgres
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    cur = conn.cursor()

    # Insert into 'location' table
    insert_sql = """
        INSERT INTO public.location (person_id, coordinate, creation_time)
        VALUES (%s, ST_Point(%s, %s), %s)
    """
    cur.execute(
        insert_sql,
        (
            location_dict["person_id"],
            location_dict["longitude"],
            location_dict["latitude"],
            datetime.now().isoformat()
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    print("[CONSUMER] Inserted new location record successfully!")
