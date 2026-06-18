from PyQt6.QtCore import QThread, pyqtSignal
from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP, ICMP
from security_core import SecurityEngine

class SnifferThread(QThread):
    packet_captured = pyqtSignal(dict)
    alert_triggered = pyqtSignal(str)

    def __init__(self, interface=None, parent=None):
        super().__init__(parent)
        self.interface = interface
        self._is_running = False
        self.engine = SecurityEngine(time_window=5)

    def run(self):
        self._is_running = True
        sniff(
            iface=self.interface,
            prn=self.process_packet,
            store=False,
            stop_filter=self.should_stop
        )

    def process_packet(self, packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst

            packet_length = len(packet)
            dst_port = 0

            packet_data = {
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'protocol': 'Unknown',
                'info': '-'
            }

            if TCP in packet:
                dst_port = packet[TCP].dport
                packet_data['protocol'] = 'TCP'
                packet_data['info'] = f"Port: {packet[TCP].sport} -> {dst_port}"
            elif UDP in packet:
                dst_port = packet[UDP].dport
                packet_data['protocol'] = 'UDP'
                packet_data['info'] = f"Port: {packet[UDP].sport} -> {dst_port}"
            elif ICMP in packet:
                packet_data['protocol'] = 'ICMP'
                packet_data['info'] = f"Type: {packet[ICMP].type}"

            alert = self.engine.analyze_packet(src_ip, dst_port, packet_length)
            if alert:
                self.alert_triggered.emit(alert)

            self.packet_captured.emit(packet_data)

    def should_stop(self, packet):
        return not self._is_running

    def stop(self):
        self._is_running = False
        self.wait()

    def reset_security_engine(self):
        return self.engine.reset_firewall()