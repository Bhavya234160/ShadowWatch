import re
import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from engine.logger import accept_event

def read_authlog(n=30):
    result = subprocess.run(["tail", f"-n{n}", "/var/log/auth.log"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    return lines if lines else []

def determine_failure(log_line):
    if "Failed password" in log_line:
        return True
    return False

def extract_ip(log_line):
    match = re.search(r'from ([\d.]+)', log_line)
    return match.group(1) if match else ""

def extract_time(log_line):
    match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)', log_line)
    if match:
        return match.group(1)
    return None

def extract_user(log_line):
    match = re.search(r'Failed password for (?:invalid user )?(\w+)', log_line)
    return match.group(1) if match else ""

def convert_to_event(log_line):
    source_ip = extract_ip(log_line)
    target_user = extract_user(log_line)
    time = extract_time(log_line) 
    event = {
        "event_type": "SSH Failure",
        "severity": "MEDIUM",
        "timestamp": time,
        "metadata": {
            "source_ip": source_ip,
            "target_user": target_user,
            "details": "Failed SSH login attempt"
        }
    }
    return event

def main():
    lines = read_authlog(50)
    events = []
    for line in lines:
        if determine_failure(line):
            event = convert_to_event(line)
            events.append(event)
            accept_event(event)
if __name__ == "__main__":
    main()