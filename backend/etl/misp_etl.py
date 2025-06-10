#!/usr/bin/env python3
import os, time, requests
from utils import send, normalize_ioc

MISP_URL = os.getenv("MISP_URL")
MISP_KEY = os.getenv("MISP_API_KEY")
INTERVAL = int(os.getenv("POLL_INTERVAL", 300))  # seconds

def fetch_and_publish():
    headers = {
        "Accept": "application/json",
        "Authorization": MISP_KEY,
        "Content-Type": "application/json",
    }
    # simple search for all attributes
    body = {"returnFormat": "json", "type": "ip-src,domain"}
    resp = requests.post(f"{MISP_URL}/attributes/restSearch", headers=headers, json=body)
    resp.raise_for_status()
    for attr in resp.json().get("response", []):
        ioc = normalize_ioc({
            "type": attr["type"],
            "value": attr["value"],
            "timestamp": attr["timestamp"],
            "raw": attr,
        }, feed="misp")
        send("cti-misp", ioc)

if __name__ == "__main__":
    while True:
        try:
            fetch_and_publish()
        except Exception as e:
            print("MISP ETL error:", e)
        time.sleep(INTERVAL)
