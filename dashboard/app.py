import json
from flask import Flask, render_template
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

INCIDENT_FILE = Path.home() / "ShadowWatch" / "logs" / "incidents.json"

app = Flask(__name__)

def read_incidents():
    if not INCIDENT_FILE.exists():
        return []
    with INCIDENT_FILE.open("r") as f:
        incidents = [json.loads(line) for line in f if line.strip()]
    return incidents

@app.route("/")
def home():
    incidents = read_incidents()
    return render_template(
        "index.html",
        total_incidents=len(incidents),
        incidents=incidents
    )
    
if __name__ == "__main__":
    app.run(debug=True)