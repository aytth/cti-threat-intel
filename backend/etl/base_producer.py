import json
import os
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv(dotenv_path=__file__[:-len("base_producer.py")] + ".env")

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP")

producer = KafkaProducer(
    bootstrap_servers=[BOOTSTRAP],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
