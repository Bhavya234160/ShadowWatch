from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.logger import accept_event

def main():
    ssh_event = {
        "event_type": "ssh_failed",
        "severity": "medium",
        "details": "Failed login",
        "event_status": "failed"
    }
    file_event = {
        "event_type": "file_modified",
        "severity": "high",
        "details": "notes.txt modified",
        "event_status": "success"
    }
    recon_event = {
        "event_type": "port_scan",
        "severity": "medium",
        "details": "Nmap scan detected",
        "event_status": "failed"
    }
    accept_event(ssh_event)
    accept_event(file_event)
    accept_event(recon_event)
    if __name__ == "__main__":
        main()