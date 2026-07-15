from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from detectors.file_detector import read_authlog, determine_failure, convert_to_event
from engine.logger import accept_event

log_lines = read_authlog(50)

for log_line in log_lines:
    if determine_failure(log_line):
        event = convert_to_event(log_line)
        accept_event(event)
        print("Successfully logged")