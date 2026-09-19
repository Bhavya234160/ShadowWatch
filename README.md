# 🛡️ ShadowWatch - Behavioral Anomaly Detection

> Learns YOUR behavior (typing, mouse, active hours) and detects impostors in real-time. Auto-locks if someone else uses your machine.

**Built for:** Privacy-first endpoint security without cloud dependency.
**Tech:** Python, pynput, psutil, Flask, SocketIO

### Why I built this?
Passwords can be stolen, but your typing rhythm & mouse patterns can't. I wanted a second layer of security that is invisible and behavioral.

<img width="1423" height="412" alt="Screenshot 2026-07-28 210027" src="https://github.com/user-attachments/assets/25d9052e-231b-45a5-9d80-122b035217a0" />
<img width="1920" height="1080" alt="Screenshot 2026-07-28 205237" src="https://github.com/user-attachments/assets/1971ed7a-d203-40e0-9c5a-1ff48a096428" />
<img width="1920" height="1080" alt="Screenshot 2026-07-23 231414" src="https://github.com/user-attachments/assets/a674b56f-28fa-4d75-954c-29e0510bf31b" />
<img width="1842" height="637" alt="Screenshot 2026-07-28 211426" src="https://github.com/user-attachments/assets/587c4823-9771-4459-b496-77015b05743f" />
<img width="1605" height="805" alt="Screenshot 2026-07-28 211212" src="https://github.com/user-attachments/assets/3d5e781b-61de-45b2-9852-c2a6edea133f" />
<img width="361" height="402" alt="Screenshot 2026-07-28 210944" src="https://github.com/user-attachments/assets/02050151-13c6-4360-8cfb-aba76b249bd6" />



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
```
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
```

## Workflow architecture
```
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
```

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
