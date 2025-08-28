from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget
from ui.styles import label_style


class InfoBar(QWidget):
    def __init__(self, parent=None):
        super(InfoBar, self).__init__(parent)

        group_box = QtWidgets.QGroupBox("Telemetri Bilgileri")
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 18px;
                border: 3px solid #1f2c51;
                border-radius: 12px;
                margin-top: 20px;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 249, 250, 0.95) 100%);
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 15px 0 15px;
                background-color: #1f2c51;
                color: white;
                border-radius: 8px;
                font-size: 16px;
            }
        """)

        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(15, 20, 15, 15)
        grid.setSpacing(20)

        # Enhanced labels with better styling
        label_style_enhanced = """
            QLabel {
                font-size: 14px;
                color: #1f2c51;
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border-radius: 10px;
                padding: 12px;
                margin: 4px;
                border: 2px solid #dee2e6;
                font-weight: 500;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        """

        # 2 rows, 3 columns with better organization
        self.location_lbl = QLabel("Konum:\n Lat 0\n Lon 0\n Alt 0")
        self.location_lbl.setStyleSheet(label_style_enhanced)
        grid.addWidget(self.location_lbl, 0, 0)

        self.attitude_lbl = QLabel("Tutum:\n Roll 0\n Pitch 0\n Yaw 0")
        self.attitude_lbl.setStyleSheet(label_style_enhanced)
        grid.addWidget(self.attitude_lbl, 0, 1)

        self.velocity_lbl = QLabel("Hız:\n Vx 0\n Vy 0\n Vz 0")
        self.velocity_lbl.setStyleSheet(label_style_enhanced)
        grid.addWidget(self.velocity_lbl, 0, 2)

        self.battery_lbl = QLabel("Batarya:\n 0V\n 0A\n Kalan %0")
        self.battery_lbl.setStyleSheet(label_style_enhanced)
        grid.addWidget(self.battery_lbl, 1, 0)

        self.gps_lbl = QLabel("GPS:\n Fix 0\n Uydu 0")
        self.gps_lbl.setStyleSheet(label_style_enhanced)
        grid.addWidget(self.gps_lbl, 1, 1)

        self.status_lbl = QLabel("Durum:\n DISARMED\n Mod: UNKNOWN")
        self.status_lbl.setStyleSheet(label_style_enhanced)
        grid.addWidget(self.status_lbl, 1, 2)

        group_box.setLayout(grid)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

    def update_info(self, data):
        loc = data.get('current_location', {})
        att = data.get('current_attitude', {})
        vel = data.get('current_velocity', {})
        bat = data.get('battery_info', {})
        gps = data.get('gps_info', {})
        armed = data.get('vehicle_armed', False)
        mode = data.get('mode', 'UNKNOWN')

        self.location_lbl.setText(f"Konum:\n Lat {loc.get('lat', 0)}\n Lon {loc.get('lon', 0)}\n Alt {loc.get('alt', 0)}")
        self.attitude_lbl.setText(f"Tutum:\n Roll {att.get('roll', 0)}\n Pitch {att.get('pitch', 0)}\n Yaw {att.get('yaw', 0)}")
        self.velocity_lbl.setText(f"Hız:\n Vx {vel.get('vx', 0)}\n Vy {vel.get('vy', 0)}\n Vz {vel.get('vz', 0)}")
        self.battery_lbl.setText(f"Batarya:\n {bat.get('voltage', 0)}V\n {bat.get('current', 0)}A\n Kalan %{bat.get('remaining', 0)}")
        self.gps_lbl.setText(f"GPS:\n Fix {gps.get('fix_type', 0)}\n Uydu {gps.get('satellites', 0)}")
        self.status_lbl.setText(f"Durum:\n {'ARMED' if armed else 'DISARMED'}\n Mod: {mode}")