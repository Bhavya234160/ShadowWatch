import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

event_json = Path.home() / "ShadowWatch" / "logs" / "events.json"
LOG_FILE = Path.home() / "ShadowWatch" / "logs" / "incidents.json"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
FILE_EVENT_TYPES = {"file_created", "file_modified", "file_deleted"}

def clear_incidents():
    if LOG_FILE.exists():
        LOG_FILE.unlink()
        
def calculate_severity(attack_chain):
    port_scan = attack_chain.get("port_scan")
    ssh_failures = attack_chain.get("ssh_failures", [])
    file_event = attack_chain.get("file_event")

    if port_scan and len(ssh_failures) > 5 and file_event:
        return "CRITICAL"
    elif port_scan and file_event:
        return "HIGH"
    elif file_event:
        return "MEDIUM"
    else:
        return "LOW"

def read_events():
    if not event_json.exists():
        return []
    with event_json.open("r") as f:
        events = [json.loads(line) for line in f if line.strip()]
    return events

def sort_events_by_timestamp(events):
    return sorted(events, key=lambda x: x.get("timestamp", ""))

def find_attack_chain(events):

    attack_chains = []

    port_scan = None
    ssh_failures = []
    file_event = None

    for event in events:

        if event["event_type"] == "port_scan":
            port_scan = event

        elif event["event_type"] == "ssh_failure":
            ssh_failures.append(event)

        elif event["event_type"] in FILE_EVENT_TYPES:
            file_event = event

        if ssh_failures and file_event:

            attack_chains.append({
                "port_scan": port_scan,
                "ssh_failures": ssh_failures.copy(),
                "file_event": file_event
            })

            ssh_failures.clear()
            file_event = None

    return attack_chains

def build_incident(attack_chain):
    port_scan = attack_chain["port_scan"]
    ssh_failures = attack_chain["ssh_failures"]
    file_event = attack_chain["file_event"]

    incident = {
        "incident_type": "multi_stage_attack",
        "severity": calculate_severity(attack_chain),
        "timestamp": (port_scan or ssh_failures[0]).get("timestamp"),
        "related_events": [
            *( [port_scan] if port_scan else [] ),
            *ssh_failures,
            file_event
        ],
        "metadata": {
            "description": "Detected a multi-stage attack involving SSH failures and file manipulation events" +
                           (" after reconnaissance." if port_scan else "."),
            "number_of_ssh_failures": len(ssh_failures),
            "file_event_type": file_event.get("event_type")
        }
    }
    return incident

def save_incident(incident):
    with LOG_FILE.open("a") as f:
        json.dump(incident, f)
        f.write("\n")
    return True

def main():
    clear_incidents()
    events = read_events()
    events = sort_events_by_timestamp(events)
    attack_chains = find_attack_chain(events)
    for attack_chain in attack_chains:
        incident = build_incident(attack_chain)
        save_incident(incident)

if __name__ == "__main__":
    main()
    
    