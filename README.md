# **UdaConnect: A Microservices-based Location Tracking System**

## **Overview**

### **Background**
UdaConnect is a microservices-based **location tracking system** designed for large conferences and events. Attendees often share common interests, but making valuable connections in crowded settings can be difficult. **UdaConnect helps attendees connect by detecting physical proximity using location data.**

### **Project Objective**
Initially developed as a **Proof of Concept (PoC)** application named **UdaTracker**, the system ingests location data and identifies users who have been in close proximity. 

The goal is to **enhance the PoC into a production-ready Minimum Viable Product (MVP)** by **refactoring the monolithic system into a scalable microservices architecture** with event-driven communication.

### **Key Features**
✅ **Real-time Location Tracking**  
✅ **Microservices Architecture** (Person, Location, Connection Services)  
✅ **Event-driven System with Kafka**  
✅ **REST & gRPC APIs**  
✅ **Kubernetes Orchestration**  
✅ **Dockerized Deployment**  
✅ **PostgreSQL with PostGIS for Geospatial Queries**  

---

## **Technology Stack**
| Technology       | Purpose |
|-----------------|---------|
| **Flask** | Web framework for REST APIs |
| **gRPC** | High-performance inter-service communication |
| **Kafka** | Message passing and event streaming |
| **PostgreSQL** | Relational database |
| **PostGIS** | Spatial database extension for PostgreSQL |
| **Docker** | Containerization |
| **Kubernetes (K3s)** | Container orchestration |
| **Vagrant & VirtualBox** | Virtualization for local development |

---

## **Project Architecture**
### **Microservices Breakdown**
The application is **refactored from a monolithic design into four microservices:**

1️⃣ **Person Service (REST API)**  
   - Manages attendee data  
   - CRUD operations for users  
   - Exposed via RESTful API  

2️⃣ **Location Service (gRPC + Kafka Producer)**  
   - Processes real-time location data  
   - Publishes location events to Kafka  

3️⃣ **Connection Service (REST API + Kafka Consumer)**  
   - Retrieves people who were in close proximity  
   - Consumes messages from Kafka  

4️⃣ **Frontend (ReactJS)**  
   - Displays event attendees and connections  

### **Infrastructure Diagram**
*(Generated from the provided architecture design files)*
![UdaConnect Architecture](architecture_design.png)

---

## **Setup & Installation**

### **1. Prerequisites**
Ensure the following dependencies are installed:
- ✅ [Docker](https://docs.docker.com/get-docker/)
- ✅ [Docker Hub Account](https://hub.docker.com/)
- ✅ [kubectl](https://kubernetes.io/docs/tasks/tools/)
- ✅ [VirtualBox 6.0+](https://www.virtualbox.org/)
- ✅ [Vagrant 2.0+](https://www.vagrantup.com/)

---

### **2. Initialize Kubernetes with K3s**
Run the following command in the project root directory:
```sh
vagrant up
```
This sets up a lightweight Kubernetes cluster on a **virtual machine using K3s**.

Once completed, SSH into the machine:
```sh
vagrant ssh
```
Retrieve the **Kubernetes config file**:
```sh
sudo cat /etc/rancher/k3s/k3s.yaml
```
Copy the output and paste it into your local `~/.kube/config` file.

Verify **kubectl**:
```sh
kubectl describe services
```
If no errors occur, Kubernetes is set up correctly.

---

### **3. Start PostgreSQL Database**
Run PostgreSQL inside a Docker container:
```sh
docker run --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=udaconnect -p 5432:5432 -d postgres
```
Apply database migrations:
```sh
python manage.py db upgrade
```

---

### **4. Start Kafka & Zookeeper**
Run Kafka and Zookeeper:
```sh
docker-compose up -d kafka zookeeper
```
Verify Kafka topics:
```sh
docker exec -it kafka /bin/sh
kafka-topics.sh --list --bootstrap-server localhost:9092
```

---

### **5. Deploy Microservices**
Apply Kubernetes manifests:
```sh
kubectl apply -f deployment/
```
Verify running pods:
```sh
kubectl get pods
```

---

## **Containerization & Deployment**

### **1. Build and Push Docker Images**
The following script automates the process of **building and pushing all microservices to Docker Hub**.

Create a file `build_and_push_all.sh` and add:
```sh
#!/bin/bash
# build_and_push_all.sh
# Usage: ./build_and_push_all.sh <DOCKERHUB_USERNAME> <TAG>

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <DOCKERHUB_USERNAME> <TAG>"
  exit 1
fi

DOCKERHUB_USERNAME=$1
TAG=$2

SERVICES=("person-service" "location-service-kafka" "location-service-grpc" "connection-service")

for service in "${SERVICES[@]}"; do
  echo "Building image for $service..."
  docker build -t "$DOCKERHUB_USERNAME/$service:$TAG" "./$service"
  
  if [ $? -ne 0 ]; then
    echo "Failed to build $service"
    exit 1
  fi
  
  echo "Pushing image $service..."
  docker push "$DOCKERHUB_USERNAME/$service:$TAG"
  
  if [ $? -ne 0 ]; then
    echo "Failed to push $service"
    exit 1
  fi
  
  echo "Successfully pushed $service"
done

echo "All images built and pushed successfully."
```
Run the script:
```sh
chmod +x build_and_push_all.sh
./build_and_push_all.sh your-dockerhub-username latest
```

---

## **Database Seeding**
Retrieve the PostgreSQL Pod Name:
```sh
kubectl get pods
```
Run the database initialization script:
```sh
sh scripts/run_db_command.sh <POD_NAME>
```

---

## **Testing**
Run unit tests:
```sh
pytest
```

Run Postman tests:
1. Import `postman.json` into **Postman**.
2. Run the test collection.

---

## **API Endpoints**
### **Person Service**
✅ **Get All Persons**  
```sh
curl -X GET http://localhost:30001/api/persons
```
✅ **Get Person by ID**  
```sh
curl -X GET http://localhost:30001/api/persons/1
```
✅ **Create a Person**  
```sh
curl -X POST http://localhost:30001/api/persons \
     -H "Content-Type: application/json" \
     -d '{"first_name": "Omar", "last_name": "Khalil", "company_name": "Udacity"}'
```

### **Connection Service**
✅ **Get Person Connections**  
```sh
curl -X GET "http://localhost:30004/api/persons/1/connection?start_date=2025-01-01&end_date=2025-12-31&distance=10"
```

---

## **Troubleshooting**
### **1. Kafka Issues**
Restart Kafka:
```sh
docker-compose down
docker-compose up -d kafka zookeeper
```

### **2. PostgreSQL Issues**
Check logs:
```sh
docker logs postgres
```

Restart the database:
```sh
docker restart postgres
```

### **3. Kubernetes Debugging**
Check logs:
```sh
kubectl logs <pod-name>
```
Restart a pod:
```sh
kubectl delete pod <pod-name>
```

---

## **Contributors**
- **Omar Khalil** - Cloud Engineer & Developer  
- **Udacity Mentors** - Support & Review  