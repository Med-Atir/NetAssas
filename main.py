import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QListWidget, QLabel, QHBoxLayout)
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QColor
from sniffer_thread import SnifferThread


class NetSniffDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetAssas - Security Dashboard (IDS/IPS)")
        self.resize(1000, 700)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; color: #ffffff; }
            QTableWidget { background-color: #2b2b2b; color: #d4d4d4; gridline-color: #3f3f46; border: 1px solid #3f3f46; }
            QHeaderView::section { background-color: #333333; color: white; padding: 4px; border: 1px solid #3f3f46; font-weight: bold; }
            QListWidget { background-color: #2b0000; color: #ff6b6b; border: 1px solid #ff0000; font-weight: bold; }
            QPushButton { padding: 8px; border-radius: 4px; font-weight: bold; }
            QLabel { color: #ffffff; font-weight: bold; font-size: 14px; margin-top: 10px; }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.sniffer_thread = SnifferThread()
        self.sniffer_thread.packet_captured.connect(self.update_traffic_table)
        self.sniffer_thread.alert_triggered.connect(self.log_alert)
        self.control_layout = QHBoxLayout()
        self.btn_toggle = QPushButton("DÉMARRER LA CAPTURE")
        self.btn_toggle.setStyleSheet("background-color: #007acc; color: white;")
        self.btn_toggle.clicked.connect(self.toggle_sniffing)
        self.control_layout.addWidget(self.btn_toggle)
        self.btn_reset = QPushButton("RÉINITIALISER LES RÈGLES")
        self.btn_reset.setStyleSheet("background-color: #d84315; color: white;")
        self.btn_reset.clicked.connect(self.reset_system)
        self.control_layout.addWidget(self.btn_reset)
        ip_label = QLabel(f"IP Locale Protégée : {self.sniffer_thread.engine.local_ip}")
        ip_label.setStyleSheet("color: #4caf50; font-style: italic;")
        self.control_layout.addWidget(ip_label)
        self.main_layout.addLayout(self.control_layout)
        self.main_layout.addWidget(QLabel("ALERTES DE SÉCURITÉ ET ACTIONS (IPS)"))
        self.alerts_list = QListWidget()
        self.alerts_list.setFixedHeight(120)
        self.main_layout.addWidget(self.alerts_list)
        self.main_layout.addWidget(QLabel("TRAFIC RÉSEAU EN TEMPS RÉEL"))
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Source IP", "Dest IP", "Protocol", "Informations"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.main_layout.addWidget(self.table)
        self.packet_counter = 0
        self.max_rows = 500

    @pyqtSlot(dict)
    def update_traffic_table(self, packet_data):
        self.packet_counter += 1
        if self.packet_counter >= self.max_rows:
            self.table.setRowCount(0)
            self.packet_counter = 0

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(packet_data['src_ip']))
        self.table.setItem(row_position, 1, QTableWidgetItem(packet_data['dst_ip']))
        proto_item = QTableWidgetItem(packet_data['protocol'])
        if packet_data['protocol'] == 'TCP':
            proto_item.setForeground(QColor('#4da6ff'))
        elif packet_data['protocol'] == 'UDP':
            proto_item.setForeground(QColor('#ffb366'))
        elif packet_data['protocol'] == 'ICMP':
            proto_item.setForeground(QColor('#ff6666'))
        self.table.setItem(row_position, 2, proto_item)
        self.table.setItem(row_position, 3, QTableWidgetItem(packet_data['info']))
        self.table.scrollToBottom()

    @pyqtSlot(str)
    def log_alert(self, message):
        self.alerts_list.addItem(message)
        self.alerts_list.scrollToBottom()

    def toggle_sniffing(self):
        if not self.sniffer_thread.isRunning():
            self.sniffer_thread.start()
            self.btn_toggle.setText("ARRÊTER LA CAPTURE")
            self.btn_toggle.setStyleSheet("background-color: #d32f2f; color: white;")
        else:
            self.sniffer_thread.stop()
            self.btn_toggle.setText("DÉMARRER LA CAPTURE")
            self.btn_toggle.setStyleSheet("background-color: #007acc; color: white;")

    def reset_system(self):
        msg = self.sniffer_thread.reset_security_engine()
        self.alerts_list.clear()
        self.table.setRowCount(0)
        self.packet_counter = 0
        self.log_alert(msg)

    def closeEvent(self, event):
        if self.sniffer_thread.isRunning():
            self.sniffer_thread.stop()
        self.sniffer_thread.reset_security_engine()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetSniffDashboard()
    window.showMaximized()
    sys.exit(app.exec())