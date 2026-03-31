# LogTrace — Forensic Incident Investigation Dashboard

> Upload a login log. Uncover the attack.

LogTrace is an open source forensic analysis tool that takes raw authentication and login log files, detects suspicious behaviour using rule-based analysis, builds an interactive timeline, and generates an analyst-style incident report — all in a browser-based dashboard.

Built as part of a cybersecurity portfolio focused on digital forensics and intelligence work.

---

## What it does

Upload a CSV or JSON log file and LogTrace will automatically:

- Detect brute force attacks — repeated failed logins from a single IP within a short time window
- Detect credential stuffing — one IP targeting many different user accounts
- Flag suspicious login hours — logins occurring outside expected activity patterns
- Identify account takeover patterns — many failed attempts followed by a successful login
- Spot lateral movement indicators — accounts accessing unusual systems post-authentication
- Build a visual timeline of all events with severity colour coding
- Generate a plain English incident report with a severity rating and recommended actions

---

## Demo

> Screenshots and a sample run using the included test dataset are in `/sample_data/`.

![Dashboard screenshot](screenshots/dashboard.png)

---

## Project structure

```
logtrace/
│
├── app.py                  # Streamlit entry point
│
├── core/
│   ├── parser.py           # Log file ingestion and cleaning
│   ├── detector.py         # Detection rules (brute force, stuffing, etc.)
│   ├── timeline.py         # Timeline builder
│   └── reporter.py         # Incident report generator
│
├── visualisation/
│   ├── charts.py           # Plotly chart functions
│   └── dashboard.py        # Streamlit layout components
│
├── sample_data/
│   ├── normal_logins.csv   # Baseline normal activity
│   ├── brute_force.csv     # Simulated brute force attack
│   └── credential_stuffing.csv
│
├── tests/
│   ├── test_parser.py
│   ├── test_detector.py
│   └── test_reporter.py
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Getting started

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/logtrace.git
cd logtrace

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

### Input format

LogTrace accepts CSV or JSON files with the following fields:

| Field | Description | Example |
|---|---|---|
| `timestamp` | Date and time of the event | `2024-03-15 02:34:11` |
| `ip_address` | Source IP address | `192.168.1.42` |
| `username` | Account targeted | `j.smith` |
| `event_type` | Login success or failure | `LOGIN_FAILED` |
| `user_agent` | Browser or client string (optional) | `Mozilla/5.0...` |

A sample dataset is included in `/sample_data/` so you can test immediately without your own logs.

---

## Detection logic

### Brute force detection
Flags any IP address that generates more than **5 failed login attempts within a 10-minute window** against the same account. Threshold is configurable in `core/detector.py`.

### Credential stuffing detection
Flags any IP address that attempts to authenticate against more than **3 different user accounts** within a 30-minute window, regardless of success or failure.

### Suspicious hour detection
Flags successful logins that occur between **00:00 and 05:00** local time, which falls outside normal usage patterns for most organisations. Configurable.

### Account takeover pattern
Flags sequences where an account sees **10 or more failed attempts followed by a successful login** within a 60-minute window — a strong indicator of a brute force success.

### Lateral movement
Flags accounts that authenticate successfully and then attempt to access systems or resources outside their normal behaviour profile within the same session window.

All thresholds are configurable. See `core/detector.py`.

---

## Incident report output

Each analysis produces a report containing:

- **Summary** — a plain English description of what happened and when
- **Severity rating** — Low / Medium / High / Critical based on a weighted scoring model
- **Indicators of Compromise (IoCs)** — IPs, usernames, and timestamps involved
- **Attack classification** — the most likely attack type based on detected patterns
- **Recommended actions** — suggested response steps for each finding
- **Exportable** — download as plain text or PDF

Example output:

```
INCIDENT REPORT — LogTrace v1.0
Generated: 2024-03-15 09:42:11
Severity: HIGH

Summary:
Analysis of the uploaded log file identified a sustained brute force attack
originating from IP 203.0.113.47 between 02:14 and 02:38 on 15 March 2024.
The attack targeted the account 'admin' with 47 failed authentication attempts
before achieving a successful login at 02:38:54.

Indicators of Compromise:
  Source IP:   203.0.113.47
  Target user: admin
  Attack start: 2024-03-15 02:14:07
  Success at:   2024-03-15 02:38:54
  Total attempts: 48 (47 failed, 1 success)

Attack classification: Brute Force — Account Compromise

Recommended actions:
  1. Immediately reset credentials for the 'admin' account
  2. Block or rate-limit IP 203.0.113.47 at the firewall
  3. Review all actions taken by the 'admin' account after 02:38:54
  4. Enable multi-factor authentication on all privileged accounts
  5. Investigate whether any data was accessed or exfiltrated
```

---

## Tech stack

| Tool | Purpose |
|---|---|
| Python | Core analysis and detection logic |
| pandas | Log parsing, cleaning, and data manipulation |
| plotly | Interactive charts and timeline visualisation |
| Streamlit | Browser-based dashboard |
| pytest | Unit testing |

---

## Roadmap

- [x] CSV log ingestion and parsing
- [x] Brute force detection
- [x] Credential stuffing detection
- [x] Suspicious hour flagging
- [x] Timeline visualisation
- [x] Incident report generation
- [ ] JSON log support
- [ ] Configurable detection thresholds via dashboard UI
- [ ] PCAP file support (network traffic analysis)
- [ ] Anomaly detection using scikit-learn (unsupervised baseline modelling)
- [ ] Multi-file comparison (compare logs across time periods)
- [ ] Export report as PDF

---

## Sample data

The `/sample_data/` directory contains synthetic log files generated using Python's `faker` library. They contain no real user data. Each file simulates a different attack scenario:

- `normal_logins.csv` — baseline normal activity with no anomalies
- `brute_force.csv` — a sustained brute force attack with eventual account compromise
- `credential_stuffing.csv` — a credential stuffing campaign across multiple accounts
- `mixed_scenario.csv` — a realistic dataset combining normal activity and attack events

---

## Disclaimer

LogTrace is built for educational purposes and security research only. It is designed to help analysts understand log-based attack detection and incident response methodology. It should only be used on log data you own or have explicit authorisation to analyse.

---

## About

Built by Erica as part of a cybersecurity portfolio.

Background in digital forensics, network analysis, and security investigation. Currently studying Computer Science at Durham University.

[GitHub](https://github.com/edsbr16) · [LinkedIn](https://linkedin.com/in/ericadasilva16)

---

## Licence

MIT License — see `LICENSE` for details.