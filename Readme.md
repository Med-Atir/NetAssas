# NetAssas: Hybrid Machine Learning IDS/IPS Architecture

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![PyQt6](https://img.shields.io/badge/UI-PyQt6-green.svg)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange.svg)
![Scikit-Learn](https://img.shields.io/badge/Model-Isolation%20Forest-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

**NetAssas** is an autonomous, real-time Intrusion Detection and Prevention System (IDS/IPS), designed specifically for Windows environments. To overcome the limitations of traditional static firewalls, this application utilizes a "Dual Filter" Artificial Intelligence architecture to analyze network traffic, detect anomalies, and actively block attackers.

This is an end-of-year project developed within the **Applied Computer Science - Data Science** program at the **Faculty of Sciences of El Jadida (Chouaïb Doukkali University)**.

---

## Core Features

- **Hybrid AI Engine (Cascaded):**
  * **Supervised Filter (XGBoost):** Ultra-fast detection of known attack signatures (DDoS, Injections, Brute Force).
  * **Unsupervised Filter (Isolation Forest):** Behavioral analysis trained solely on healthy traffic to intercept *Zero-Day* attacks and mathematical anomalies.
- **Active Prevention (IPS):** Automated interfacing with the Windows firewall (`netsh`) to instantly ban compromised IP addresses in a matter of milliseconds.
- **Interactive Dashboard:** Graphical user interface developed with **PyQt6** for dynamic supervision of IP flows, protocols, and security alerts.
- **Self-Protection:** Dynamic detection of the local IP address and automatic whitelisting to prevent the system from blocking itself.
- **Memory Optimization:** Automatic purging of the graphical RAM and AI history every 500 healthy packets to ensure rock-solid stability during continuous execution.

---

## Installation & Usage

The application has been packaged to run as a completely standalone executable on Windows, requiring no Python installation. 
*A Linux version will be available in the future, Inshallah.*

### 1. Mandatory Prerequisite
For network packet capture to function on Windows, you **must** have a network capture driver installed, such as **Npcap** (which is typically included with Wireshark).
- [Download Npcap](https://npcap.com/#download)

### 2. Launching the App
1. Navigate to the **Releases** tab of this GitHub repository.
2. Download the `.zip` archive containing the executable.
3. Extract the folder to your desktop.
4. Double-click on `NetAssas.exe`.
5. **Crucial:** Accept the Administrator rights prompt (UAC). Admin privileges are mandatory to allow the software to inject blocking rules into the system firewall.

---

## For Developers

If you wish to modify the source code or recompile the application yourself:

### 1. Environment Setup

```bash
# Clone the repository
git clone [https://github.com/ISAGIBD4/NetAssas.git](https://github.com/ISAGIBD4/NetAssas.git)
cd NetAssas

# Create and activate the virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install the required dependencies
pip install -r requirements.txt
```

### 2. AI Training (Optional)

Run the provided training script on a Cloud platform (like Kaggle) using the reference datasets (CIC-IDS-2018 / UNSW-NB15) to generate the 5 required artifacts:

- `ids_scaler.pkl`
- `ids_encoder.pkl`
- `modele_supervise.pkl`
- `modele_non_supervise.pkl`
- `ids_features.pkl`

Place these 5 files in the root directory of the project.

### 3. Compilation with PyInstaller

To regenerate the Windows executable with embedded administrator rights:

```bash
pip install pyinstaller
pyinstaller NetAssas.spec
```

The final executable will be generated inside the `dist/NetAssas/` directory.

---

## Project Structure

```text
NetAssas/
│
├── main.py                # Application entry point and GUI (PyQt6)
├── sniffer_thread.py      # Asynchronous network capture thread (Scapy)
├── security_core.py       # Hybrid AI engine and prevention logic (IPS)
│
├── *.pkl                  # Pre-trained Machine Learning models (Not included in source code)
├── NetAssas.spec          # PyInstaller compilation configuration
├── requirements.txt       # Exact list of required Python dependencies
└── README.md              # Project documentation
```

---

## License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

*Note on Third-Party Libraries:*
*   **PyQt6**: Utilized under the GNU GPLv3 license.
*   **Scikit-Learn, XGBoost, Scapy**: Utilized under their respective permissive open-source licenses (BSD/MIT).

Developed by **Mohammed Atir**.
