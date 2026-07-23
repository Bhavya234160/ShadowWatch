import time
import os
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from engine.logger import accept_event

USERNAME = os.getenv("USER") or os.getenv("LOGNAME") or "user"
TARGET_FOLDER = f"/home/{USERNAME}/Important"

SEVERITY_MAP = {
    "passwords.txt" : "CRITICAL",
    "config.json" : "HIGH",
    "secrets.env" : "HIGH",
    "employee.db" : "MEDIUM",
    "notes.txt" : "LOW"
}

def build_event(event_type, file_path):
    filename = os.path.basename(file_path)
    severity = SEVERITY_MAP.get(filename, "NOT CONFIRMED")
    event = {
        "event_type": event_type,
        "severity": severity,
        "timestamp": datetime.now().astimezone().isoformat(),
        "metadata": {
            "file_name": filename,
            "path_to_file": file_path,
            "operation_type": f"{filename} was {event_type.replace('file_', '')}."
        }
    }
    return event

class ImportantFolderHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"[CREATED] {event.src_path}")
            event_data = build_event("file_created", event.src_path)
            accept_event(event_data)
    
    def on_modified(self, event):
        if not event.is_directory:
            print(f"[MODIFIED] {event.src_path}")
            event_data = build_event("file_modified", event.src_path)
            accept_event(event_data)
            
    def on_deleted(self, event):
        if not event.is_directory:
            print(f"[DELETED] {event.src_path}")
            event_data = build_event("file_deleted", event.src_path)
            accept_event(event_data)
            
def main():
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
        print(f"[+] Created monitoring folder: {TARGET_FOLDER}")

    event_handler = ImportantFolderHandler()
    observer = Observer()
    observer.schedule(event_handler, path=TARGET_FOLDER, recursive=False)
    observer.start()
    print(f"[*] Watching {TARGET_FOLDER} for creation, modification, and deletion...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()        