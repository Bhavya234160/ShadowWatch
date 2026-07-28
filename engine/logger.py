import json
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path.home() / "ShadowWatch" / "logs" / "events.json"

def accept_event(event):
    if not isinstance(event, dict):
        raise ValueError("Event must be a dictionary")
    if "event_type" not in event:
        raise ValueError("Event must have an 'event_type' field")
    if "timestamp" not in event:
        event["timestamp"] = datetime.now(timezone.utc).isoformat()
    if "severity" not in event:
        raise ValueError("Event must have a 'severity' field")

    with LOG_FILE.open("a") as f:
        json.dump(event, f)
        f.write("\n")
    return True

def clear_events():
    if LOG_FILE.exists():
        LOG_FILE.unlink()
