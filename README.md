# ShadowWatch

ShadowWatch is a lightweight SIEM (Security Information and Event Management) system built using Python. The purpose of this project is to monitor different security events, correlate them together, and generate security incidents through a simple web dashboard.
This project was built as a cybersecurity learning project to understand how SIEM tools work internally. Instead of relying on existing SIEM solutions, I tried to build a simplified version from scratch.

## Features

 SSH brute-force attack detection
 Port scan detection using Nmap XML reports
 File integrity monitoring
 Event logging in JSON format
 Correlation engine for detecting multi-stage attacks
 Incident generation with severity levels
 Flask dashboard to visualize incidents

## Tech Stack

 Python
 Flask
 HTML
 CSS
 JavaScript
 Watchdog
 Nmap
 JSON
 Linux (Ubuntu & Kali)

## Project Structure

ShadowWatch/
│
├── dashboard/
│   ├── templates/
│   ├── static/
│   └── app.py
│
├── detectors/
│   ├── ssh_detector.py
│   ├── recon_detector.py
│   └── file_detector.py
│
├── engine/
│   ├── correlator.py
│   ├── incident.py
│   └── logger.py
│
├── logs/
│   ├── events.json
│   └── incidents.json
│
├── recon/
│   └── scan_results.xml
|
│── tests/
│   ├── test_file_detector.py
│   ├── test_logger.py
│   └── test_ssh_detector.py
|
├── controller.py
│
└── README.md

## Workflow architecture

                +----------------+
                |   Attacker     |
                | Kali Linux/WSL |
                +-------+--------+
                        |
        SSH / Nmap / File Activity
                        |
                        v
+----------------------------------------+
|              ShadowWatch               |
|                                        |
| SSH Detector                           |
| Recon Detector                         |
| File Detector                          |
|                |                       |
|                v                       |
|        Correlation Engine              |
|                |                       |
|                v                       |
|        Incident Generator              |
+----------------+-----------------------+
                 |
                 v
         Flask Dashboard

## How It Works

The project collects security events from multiple detectors.
- SSH Detector checks authentication logs for failed login attempts.
- Recon Detector analyzes Nmap XML scan reports.
- File Detector monitors important files and folders.
- All events are stored inside `events.json`.
- The Correlation Engine reads these events and combines related activities into a single incident.
- The dashboard displays the generated incidents.

## Future Improvements

Some improvements I would like to add in future are:
- Email alerts
- Real-time dashboard updates
- More attack detectors
- Better correlation rules
- Database support
- Docker deployment

## Learning Outcome

This project helped me improve my knowledge in:
- Cybersecurity fundamentals
- Security monitoring
- Python programming
- Flask
- Linux
- Event correlation
- JSON logging
- Software architecture

## Author

Bhavya Kuryawat
B.Tech Computer Science and Engineering
National Institute of Technology Sikkim
Interested in Cybersecurity and Security Engineering.
