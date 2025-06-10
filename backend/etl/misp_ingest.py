import os, time
from pymisp import PyMISP
from base_producer import producer
from datetime import datetime

MISP_URL = os.getenv("MISP_URL")
MISP_KEY = os.getenv("MISP_KEY")

misp = PyMISP(MISP_URL, MISP_KEY, ssl=False)

def fetch_and_publish():
    # Fetch the latest attributes
    events = misp.search_index(limit=100) 
    for evt in events:
        event_id = evt.get("Event", {}).get("id")
        attrs = misp.get_event_attributes(event_id)
        for a in attrs:
            msg = {
                "type": a.get("type"),
                "value": a.get("value"),
                "feed": "misp",
                "first_seen": a.get("timestamp"),
                "fetched_at": int(time.time())
            }
            producer.send("cti-misp", msg)
    producer.flush()

if __name__ == "__main__":
    while True:
        fetch_and_publish()
        time.sleep(300)  # every 5 minutes
