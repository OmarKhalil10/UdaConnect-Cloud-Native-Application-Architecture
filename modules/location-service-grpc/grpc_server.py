import time
from concurrent import futures
import grpc
import location_pb2
import location_pb2_grpc
import json
from kafka import KafkaProducer
import os

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        grpc_data = {
            "person_id": int(request.person_id),
            "longitude": request.longitude,
            "latitude": request.latitude,
        }
        print("[gRPC SERVER] Received:", grpc_data)
        self.forward_to_kafka(grpc_data)
        
        # Return the same data as a gRPC response
        return location_pb2.LocationMessage(**grpc_data)

    def forward_to_kafka(self, data):
        producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER])
        message_bytes = json.dumps(data).encode("utf-8")
        producer.send(TOPIC_NAME, message_bytes)
        producer.flush()
        print("[gRPC SERVER] Forwarded message to Kafka!")

# Initialize the gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

print("[gRPC SERVER] Starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
    print("[gRPC SERVER] Stopped.")
