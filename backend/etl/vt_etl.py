#!/usr/bin/env python3
import os, time, requests
from utils import send, normalize_ioc

VT_KEY = os.getenv("VT_API_KEY")
INTERVAL = int(os.getenv("POLL_INTERVAL", 300))

def fetch_and_publish():
    headers = {"x-apikey": VT_KEY}
    # example: fetch recent file IOCs (you’ll need to adjust to VT’s URL)
    resp = requests.get("https://www.virustotal.com/api/v3/intelligence/search", headers=headers, params={"query":"malware"})
    resp.raise_for_status()
    for item in resp.json().get("data", []):
        rec = normalize_ioc({
            "type": item["type"],
            "value": item["id"],
            "first_seen": item["attributes"]["first_submission_date"],
            "raw": item,
        }, feed="virustotal")
        send("cti-virustotal", rec)

if __name__ == "__main__":
    while True:
        try:
            fetch_and_publish()
        except Exception as e:
            print("VT ETL error:", e)
        time.sleep(INTERVAL)
