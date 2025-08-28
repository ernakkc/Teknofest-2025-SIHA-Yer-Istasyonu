from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QWidget, QGroupBox
from ui.styles import button_style, secondary_button_style, combo_style, status_label_style, error_label_style

import serial.tools.list_ports


class Connector(QWidget):
    def __init__(self, parent=None, connect_func=None):
        super(Connector, self).__init__(parent)
        self.connect_func = connect_func

        # Main vertical layout with better spacing
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(15)

        # Status label with better styling
        self.status_label = QLabel("Bağlantı Durumu: Bağlı Değil")
        self.status_label.setStyleSheet(error_label_style)
        main_layout.addWidget(self.status_label)

        # Group box for connection settings
        group_box = QGroupBox("Seri Port Ayarları")
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #1f2c51;
                border-radius: 10px;
                margin-top: 15px;
                background-color: rgba(255, 255, 255, 0.95);
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: #1f2c51;
                color: white;
                border-radius: 5px;
            }
        """)

        group_layout = QVBoxLayout()
        group_layout.setSpacing(12)

        # Port selection
        port_layout = QHBoxLayout()
        port_layout.setSpacing(10)
        port_label = QLabel("Port:")
        port_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        port_layout.addWidget(port_label)

        self.port_combo = QComboBox()
        self.port_combo.setStyleSheet(combo_style)
        ports = serial.tools.list_ports.comports()
        available_ports = [port.device for port in ports]
        if available_ports:
            self.port_combo.addItems(available_ports)
        else:
            self.port_combo.addItem("No ports available")
        self.port_combo.setToolTip("Seri port seçiniz")
        port_layout.addWidget(self.port_combo)
        group_layout.addLayout(port_layout)

        # Baud rate selection
        baud_layout = QHBoxLayout()
        baud_layout.setSpacing(10)
        baud_label = QLabel("Baud Rate:")
        baud_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        baud_layout.addWidget(baud_label)

        self.baud_combo = QComboBox()
        self.baud_combo.setStyleSheet(combo_style)
        self.baud_combo.addItems(["9600", "19200", "38400", "57600", "115200", "921600"])
        self.baud_combo.setCurrentText("57600")
        self.baud_combo.setToolTip("Baud rate seçiniz")
        baud_layout.addWidget(self.baud_combo)
        group_layout.addLayout(baud_layout)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.connect_button = QPushButton("Bağlan")
        self.connect_button.setStyleSheet(button_style)
        self.connect_button.clicked.connect(self.connect)
        buttons_layout.addWidget(self.connect_button)

        self.refresh_button = QPushButton("Yenile")
        self.refresh_button.setStyleSheet(secondary_button_style)
        self.refresh_button.clicked.connect(self.refresh_ports)
        buttons_layout.addWidget(self.refresh_button)

        group_layout.addLayout(buttons_layout)
        group_box.setLayout(group_layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

    def update_status(self, connected):
        self.status_label.setText("Bağlantı Durumu: Bağlı" if connected else "Bağlantı Durumu: Bağlı Değil")

    def refresh_ports(self):
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        available_ports = [port.device for port in ports]
        if available_ports:
            self.port_combo.addItems(available_ports)
        else:
            self.port_combo.addItem("No ports available")

    def get_selected_port(self):
        return self.port_combo.currentText()

    def get_selected_baudrate(self):
        return self.baud_combo.currentText()

    def connect(self):
        selected_port = self.get_selected_port()
        selected_baudrate = self.get_selected_baudrate()
        # Implement the connection logic here
        if self.connect_func(selected_port, selected_baudrate):
            self.update_status(True)
        else:
            self.update_status(False)
