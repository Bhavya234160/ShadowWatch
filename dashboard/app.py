import json
import subprocess
from flask import redirect, url_for, Flask, render_template, flash

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from ShadowWatch.controller import run_scan
INCIDENT_FILE = Path.home() / "ShadowWatch" / "logs" / "incidents.json"

app = Flask(__name__)
app.secret_key = "supersecretkey123" 
detector_processes = {}

def read_incidents():
    if not INCIDENT_FILE.exists():
        return []
    with INCIDENT_FILE.open("r") as f:
        incidents = [json.loads(line) for line in f if line.strip()]
    return incidents

@app.route("/")
def home():
    incidents = read_incidents()
    total_incidents = len(incidents)
    critical = sum(1 for i in incidents if i.get("severity") == "CRITICAL")
    high = sum(1 for i in incidents if i.get("severity") == "HIGH")
    medium = sum(1 for i in incidents if i.get("severity") == "MEDIUM")
    low = sum(1 for i in incidents if i.get("severity") == "LOW")
    return render_template(
        "index.html",
        incidents=incidents,
        total_incidents=total_incidents,
        critical=critical,
        high=high,
        medium=medium,
        low=low
    )
    
@app.route("/incident/<int:incident_id>")
def incident_details(incident_id):

    incidents = read_incidents()

    if incident_id >= len(incidents):
        return "Incident not found",404

    return render_template(
        "index.html",
        incident=incidents[incident_id]
    )

@app.route("/scan", methods=["POST"])
def scan():
    messages = run_scan()
    for msg in messages:
        flash(msg)

    return redirect(url_for("home"))
    
if __name__ == "__main__":
    app.run(debug=True)