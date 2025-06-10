#!/usr/bin/env python3
import os, time, requests
from utils import send, normalize_ioc

OTX_KEY = os.getenv("OTX_API_KEY")
INTERVAL = int(os.getenv("POLL_INTERVAL", 300))

def fetch_and_publish():
    headers = {"X-OTX-API-KEY": OTX_KEY}
    # fetch the last 50 pulses
    resp = requests.get("https://otx.alienvault.com/api/v1/pulses", headers=headers, params={"limit":50})
    resp.raise_for_status()
    for pulse in resp.json().get("results", []):
        for ioc in pulse.get("indicators", []):
            rec = normalize_ioc({
                "type": ioc["indicator_type"],
                "value": ioc["indicator"],
                "first_seen": ioc["created"],
                "raw": ioc,
            }, feed="otx")
            send("cti-otx", rec)

if __name__ == "__main__":
    while True:
        try:
            fetch_and_publish()
        except Exception as e:
            print("OTX ETL error:", e)
        time.sleep(INTERVAL)
