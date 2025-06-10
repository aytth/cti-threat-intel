import os, time
from OTXv2 import OTXv2
from base_producer import producer

OTX_KEY = os.getenv("OTX_KEY")
otx = OTXv2(OTX_KEY)

def fetch_and_publish():
    pulses = otx.getall(offset=0)  # parameter can be changed 
    for pulse in pulses:
        for ind in pulse.get("indicators", []):
            msg = {
                "type": ind.get("type"),
                "value": ind.get("indicator"),
                "feed": "otx",
                "first_seen": ind.get("modified"),
                "fetched_at": int(time.time())
            }
            producer.send("cti-otx", msg)
    producer.flush()

if __name__ == "__main__":
    while True:
        fetch_and_publish()
        time.sleep(300)
