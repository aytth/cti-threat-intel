import os, time, requests
from base_producer import producer

ENDPOINT = os.getenv("SIEM_ENDPOINT")
USER     = os.getenv("SIEM_USER")
PASS     = os.getenv("SIEM_PASS")

def fetch_and_publish():
    resp = requests.get(ENDPOINT, auth=(USER, PASS))
    resp.raise_for_status()
    logs = resp.json()
    for entry in logs:
        msg = {
            "timestamp": entry.get("timestamp"),
            "host": entry.get("host"),
            "message": entry.get("message"),
            "level": entry.get("level", "info"),
            "fetched_at": int(time.time())
        }
        producer.send("siem-logs", msg)
    producer.flush()

if __name__ == "__main__":
    while True:
        fetch_and_publish()
        # Every 1min SIEM feed is pulled
        time.sleep(60) 
