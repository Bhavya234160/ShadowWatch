import os
import json
from datetime import datetime, timezone

LOG_FILE = os.path.expanduser("~/ShadowWatch/logs/events.json")

def accept_event(event):
    if not isinstance(event, dict):
        raise ValueError("Event must be a dictionary")
    if "event_type" not in event:
        raise ValueError("Event must have an 'event_type' field")
    if "timestamp" not in event:
        event["timestamp"] = datetime.now(timezone.utc).isoformat()
    if "severity" not in event:
        raise ValueError("Event must have a 'severity' field")
    
    with open(LOG_FILE, "a") as f:
        json.dump(event, f)
        f.write("\n")

    return True
