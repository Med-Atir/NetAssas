import subprocess
import time
from collections import defaultdict
import joblib
import numpy as np
import warnings
import socket

warnings.filterwarnings("ignore", category=UserWarning)


class SecurityEngine:
    def __init__(self, time_window=5):
        self.time_window = time_window
        self.traffic_history = defaultdict(list)
        self.blocked_ips = set()
        self.local_ip = self._get_local_ip()
        self.whitelist = ["127.0.0.1", "0.0.0.0", "255.255.255.255", self.local_ip]
        self.normal_packet_count = 0

        print(f"[INFO] IP Locale auto-détectée et mise sur liste blanche : {self.local_ip}")
        print("[INFO] Démarrage de l'Intelligence Artificielle NetAssas...")

        try:
            self.scaler = joblib.load('ids_scaler.pkl')
            self.encoder = joblib.load('ids_encoder.pkl')
            self.xgb_model = joblib.load('modele_supervise.pkl')
            self.iso_model = joblib.load('modele_non_supervise.pkl')
            self.features = joblib.load('ids_features.pkl')
            self.ai_ready = True
            print("[INFO] Modèles IA chargés avec succès (Hybride Prêt) !")
        except Exception as e:
            print(f"[ERREUR] Impossible de charger les modèles IA : {e}")
            self.ai_ready = False

    def _get_local_ip(self):
        """Détecte l'adresse IP dynamique de la machine pour éviter de s'auto-bloquer."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def analyze_packet(self, src_ip, dst_port, packet_length):
        if src_ip in self.blocked_ips or src_ip in self.whitelist or not self.ai_ready:
            return None

        current_time = time.time()
        self.traffic_history[src_ip] = [
            (t, p, l) for t, p, l in self.traffic_history[src_ip]
            if current_time - t < self.time_window
        ]
        self.traffic_history[src_ip].append((current_time, dst_port, packet_length))

        total_packets = len(self.traffic_history[src_ip])
        if total_packets > 5:
            avg_length = sum(l for t, p, l in self.traffic_history[src_ip]) / total_packets
            features_brutes = np.array([[dst_port, total_packets, avg_length]])
            features_scaled = self.scaler.transform(features_brutes)
            prediction_xgb = self.xgb_model.predict(features_scaled)
            label_predit = self.encoder.inverse_transform(prediction_xgb)[0]

            if label_predit == 'ATTACK':
                self.block_ip(src_ip)
                return f"[XGBoost] Signature d'attaque reconnue ! IP {src_ip} bloquée."

            prediction_iso = self.iso_model.predict(features_scaled)
            if prediction_iso[0] == -1:
                self.block_ip(src_ip)
                return f"[Comportemental] Trafic anormal détecté (Zero-Day suspecté) ! IP {src_ip} bloquée."

        self.normal_packet_count += 1
        if self.normal_packet_count >= 500:
            self.traffic_history.clear()
            self.normal_packet_count = 0

        return None

    def block_ip(self, ip):
        """Bloque l'IP dans le pare-feu Windows via CMD."""
        if ip not in self.blocked_ips:
            self.blocked_ips.add(ip)
            try:
                rule_name = f"NetSniff_Block_{ip}"
                cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip}'
                subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"Erreur IPS pour {ip}: {e}")

    def reset_firewall(self):
        """Purge les règles et la mémoire."""
        if not self.blocked_ips:
            return "[INFO] Aucune règle à réinitialiser."

        compte = 0
        for ip in self.blocked_ips:
            try:
                cmd = f'netsh advfirewall firewall delete rule name="NetSniff_Block_{ip}" dir=in'
                subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                compte += 1
            except:
                pass

        self.blocked_ips.clear()
        self.traffic_history.clear()
        self.normal_packet_count = 0
        return f"[SYSTÈME] Succès : {compte} IP(s) débloquée(s) et mémoire purgée."