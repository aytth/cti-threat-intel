import os, time, requests
from base_producer import producer

VT_KEY    = os.getenv("VT_KEY")
VT_FEED   = os.getenv("VT_FEED_URL")
HEADERS   = {"x-apikey": VT_KEY}

def fetch_and_publish():
    resp = requests.get(VT_FEED, headers=HEADERS)
    resp.raise_for_status()
    for line in resp.iter_lines():
        if not line: continue
        record = line.decode("utf-8").split(",")  # parsing parameter can be adjusted
        msg = {
            "type": record[0],
            "value": record[1],
            "feed": "virustotal",
            "first_seen": record[2],
            "fetched_at": int(time.time())
        }
        producer.send("cti-virustotal", msg)
    producer.flush()

if __name__ == "__main__":
    while True:
        fetch_and_publish()
        time.sleep(300)
