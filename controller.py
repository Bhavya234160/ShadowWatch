from pathlib import Path
from detectors import file_detector
from detectors import ssh_detector
from detectors import recon_detector
from engine.correlator import main as correlate
from engine.logger import clear_events

ROOT = Path(__file__).resolve().parent

def run_scan():

    status = []

    clear_events()

    try:
        file_detector.main()
        status.append("✓ File Detector Complete")
    except Exception as e:
        status.append(f"❌ File Detector Failed: {e}")

    try:
        ssh_detector.main()
        status.append("✓ SSH Detector Complete")
    except Exception as e:
        status.append(f"❌ SSH Detector Failed: {e}")

    xml = ROOT / "recon" / "scan_results.xml"

    if xml.exists():
        try:
            recon_detector.main(str(xml))
            status.append("✓ Recon Detector Complete")
        except Exception as e:
            status.append(f"❌ Recon Detector Failed: {e}")
    else:
        status.append("⚠ Recon XML Missing")

    try:
        correlate()
        status.append("✓ Correlation Complete")
    except Exception as e:
        status.append(f"❌ Correlation Failed: {e}")

    return status