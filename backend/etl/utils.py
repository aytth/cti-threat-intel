import os, json
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()  # loads .env in etl/

BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
producer = KafkaProducer(
    bootstrap_servers=[BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def send(topic: str, record: dict):
    """Send a Python dict to Kafka topic."""
    producer.send(topic, record)
    producer.flush()

def normalize_ioc(raw: dict, feed: str) -> dict:
    """Build our canonical IOC record."""
    return {
        "type": raw.get("type"),
        "value": raw.get("value"),
        "feed": feed,
        "first_seen": raw.get("first_seen", raw.get("timestamp")),
        "raw": raw,
    }
