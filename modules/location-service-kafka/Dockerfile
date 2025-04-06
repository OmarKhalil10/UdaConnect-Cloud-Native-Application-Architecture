FROM python:3.8

WORKDIR /location-service-kafka

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "consumer.py"]