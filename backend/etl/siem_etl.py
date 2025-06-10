#!/usr/bin/env python3
import os, time, json
from utils import send

LOGFILE = os.getenv("SIEM_LOG_FILE", "/var/log/siem.json")
INTERVAL = 1

def tail_and_publish():
    with open(LOGFILE) as f:
        f.seek(0,2)  # EOF
        while True:
            line = f.readline()
            if not line:
                time.sleep(INTERVAL)
                continue
            try:
                evt = json.loads(line)
            except json.JSONDecodeError:
                continue
            record = {
                "timestamp": evt.get("@timestamp"),
                "host": evt.get("host"),
                "message": evt,
            }
            send("siem-logs", record)

if __name__ == "__main__":
    tail_and_publish()
