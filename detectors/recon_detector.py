import xml.etree.ElementTree as ET
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from engine.logger import accept_event


def read_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root
          
def build_event(root):
    hosts = []
    timestamp = None
    for host in root.findall("host"):
        address = host.find("address").get("addr")
        times = host.find("times")
        target_ip = address
        timestamp = root.get("startstr")            
        ports = []
        for port in host.findall("ports/port"):
            ports.append({
                "port": port.get("portid"),
                "state": port.find("state").get("state")
            })
        hosts.append({
            "host": address,
            "ports": ports
        })
    if not hosts:
        return []
       
    open_ports = []
    for host in hosts:
        for port in host["ports"]:
            if port["state"] == "open":
                open_ports.append((host["host"], port["port"]))
                
    total_ports = len(open_ports)
    if total_ports < 5:
        severity = "LOW"
    elif total_ports < 10:
        severity = "MEDIUM"
    else:
        severity = "HIGH"
    number_of_ports_scanned = sum(len(host["ports"]) for host in hosts)
   
    event = {
        "event_type": "port_scan",
        "severity": severity,
        "timestamp": timestamp,
        "target_ip": target_ip,
        "details": f"Detected a port scan with {len(hosts)} hosts and {number_of_ports_scanned} ports scanned.",
        "metadata": {
            "host_count": len(hosts),
            "ports_scanned": number_of_ports_scanned,
            "open_ports": open_ports,
        }
    }

    return [event]

def main():
    xml_file = "scan_results.xml"
    root = read_xml(xml_file)
    events = build_event(root)
    for event in events:
        accept_event(event)

if __name__ == "__main__":
    main()