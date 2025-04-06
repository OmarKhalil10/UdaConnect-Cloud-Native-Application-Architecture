import grpc
import location_pb2
import location_pb2_grpc
import os

"""
Sample location generator that writes messages to a gRPC service.
"""

# If needed, let the host/port be environment-driven:
GRPC_HOST = os.environ.get("GRPC_HOST", "localhost")
GRPC_PORT = os.environ.get("GRPC_PORT", "5005")

channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
stub = location_pb2_grpc.LocationServiceStub(channel)

print("[GENERATOR] Sending sample payload to gRPC...")

# Example payload
location = location_pb2.LocationMessage(
    person_id=1,
    longitude="-122.290883",
    latitude="37.55363",
)

response = stub.Create(location)
print("[GENERATOR] gRPC response:", response)
