# NetAssas: ML-Assisted Packet Sniffer & Traffic Analyzer

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![PyQt6](https://img.shields.io/badge/UI-PyQt6-green.svg)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange.svg)
![Scikit-Learn](https://img.shields.io/badge/Model-Isolation%20Forest-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

**NetAssas** is a real-time network packet sniffer and traffic analyzer built for Windows environments. Combining live packet capture via **Scapy** with lightweight Machine Learning inference (**XGBoost** and **Isolation Forest**), it inspects live network frames, flags suspicious traffic patterns, and provides optional host-level IP blocking through the Windows Firewall.

This project was developed as an end-of-year capstone within the **Applied Computer Science (DEUG)** program at the **Faculty of Sciences of El Jadida (Chouaïb Doukkali University)**.

---

## Core Features

- **Real-Time Packet Capture & Inspection:** Asynchronous packet sniffing powered by **Scapy** and **Npcap**, decoding Ethernet, IP, TCP, UDP, and ICMP headers on live Windows network interfaces.
- **ML-Assisted Traffic Classification:**
  - **Signature Scoring (XGBoost):** Evaluates extracted packet/session attributes to flag known suspicious traffic patterns (floods, brute-force bursts, anomalous scans).
  - **Outlier Scoring (Isolation Forest):** Unsupervised model trained on baseline traffic to highlight statistical deviations from normal host activity.
- **Automated Host Containment:** Optional integration with Windows Firewall (`netsh`) to block flagged remote IP addresses at the host level.
- **Interactive PyQt6 Dashboard:** Live packet feed, protocol distribution monitoring, and alert logging built with **PyQt6**.
- **Self-Protection & Memory Management:** Automatically detects and whitelists the local host IP to prevent self-lockout, and periodically purges buffered packet history every 500 clean packets to maintain a low memory footprint.

---

## Installation & Usage

The application is packaged as a standalone Windows executable requiring no local Python environment.

### 1. Mandatory Prerequisite
Live packet capture on Windows requires **Npcap** (commonly bundled with Wireshark):
- [Download Npcap](https://npcap.com/#download) *(install with WinPcap API-compatible Mode enabled)*

### 2. Launching the App
1. Navigate to the **Releases** tab of this repository.
2. Download and extract the `.zip` archive to your desktop.
3. Run `NetAssas.exe`.
4. **Administrator Privileges:** Accept the Windows UAC prompt if you intend to capture raw network interfaces and apply `netsh` firewall rules.

---

## For Developers

### 1. Environment Setup

```bash
git clone [https://github.com/ISAGIBD4/NetAssas.git](https://github.com/ISAGIBD4/NetAssas.git)
cd NetAssas

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Model Artifacts

Place the pre-trained model and preprocessing artifacts in the project root directory before running or packaging:
- `ids_scaler.pkl`
- `ids_encoder.pkl`
- `modele_supervise.pkl`
- `modele_non_supervise.pkl`
- `ids_features.pkl`

### 3. Building the Windows Executable

```bash
pip install pyinstaller
pyinstaller NetAssas.spec
```

The standalone bundle will be generated inside `dist/NetAssas/`.

---

## Project Structure

```text
NetAssas/
│
├── main.py                # Application entry point and PyQt6 GUI
├── sniffer_thread.py      # Asynchronous packet capture worker (Scapy)
├── security_core.py       # Feature extraction, ML scoring, and netsh blocker
│
├── *.pkl                  # Pre-trained ML artifacts (excluded from repository)
├── NetAssas.spec          # PyInstaller build configuration
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

*Third-Party Libraries:*
- **PyQt6**: Used under the GNU GPLv3 license.
- **Scikit-Learn, XGBoost, Scapy**: Used under their respective permissive open-source licenses (BSD/MIT).

Developed by **Mohammed Atir**.
