import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QScrollArea, QFrame
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer

from utils.siha_controller import SIHAController

from ui.infobar import InfoBar
from ui.connector import Connector
from ui.video import VideoFeed
from ui.map import MapWidget
from ui.console import ConsoleWidget
from ui.modselector import ModSelector
from ui.armer import Armer
from ui.kacis_manevra import KacisManevra
from ui.hiz_gonder import HizGonder
from ui.yuksel import Yuksel
from ui.otonom_ui import Otonom_UI

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.siha = SIHAController()
        self.initUI()

        # Set window properties - more reasonable size
        self.setWindowTitle("SIHA Yer Kontrol İstasyonu")
        self.setMinimumSize(1200, 700)
        self.resize(1400, 800)  # Default size
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        # Apply modern gradient background
        palette = QPalette()
        gradient = "background: background: linear-gradient(90deg, #1f2c51, #1f2c51, #1f2c51);"
        self.setStyleSheet(f"""
            QWidget {{
                {gradient}
                color: white;
            }}
            QScrollBar:vertical {{
                background-color: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: rgba(255, 255, 255, 0.5);
            }}
        """)

        self.siha.update_telemetry()
        self.info_bar.update_info(self.siha.return_telemetry_var())

        # Welcome message in console
        print(" SIHA Yer Kontrol İstasyonu başlatıldı!")
        print(" Sistem hazır - Telemetri verilerini izlemeye başlayın")
        print(" Kontrol panelinden komutlarınızı gönderin")

        # Start periodic telemetry updates
        self.start_telemetry_timer()



    def initUI(self):
        # Main horizontal layout - split screen approach
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

        # Left side - Video and Telemetry (fixed width)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)  # Fixed proportion

        # Right side - Controls (scrollable, flexible width)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)  # Fixed proportion

    def create_left_panel(self):
        """Create left panel with video, map and telemetry"""
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)
        panel.setLayout(layout)

        # Title
        title_label = QLabel(" SIHA Kontrol")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: black;
                padding: 8px;
                border-radius: 8px;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Video and Map side by side
        media_layout = QHBoxLayout()
        media_layout.setSpacing(8)

        # Video feed
        self.video_feed = VideoFeed()
        media_layout.addWidget(self.video_feed)

        # Map widget
        self.map_widget = MapWidget()
        media_layout.addWidget(self.map_widget)

        layout.addLayout(media_layout)

        # Telemetry info
        self.info_bar = InfoBar(self)
        layout.addWidget(self.info_bar)

        # Console for logs and outputs
        self.console_widget = ConsoleWidget()
        layout.addWidget(self.console_widget)

        return panel

    def create_right_panel(self):
        """Create right panel with all controls in scroll area"""
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)
        panel.setLayout(layout)

        # Controls title
        controls_title = QLabel("🎮 Kontrol Paneli")
        controls_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: black;
                padding: 5px;
                border-radius: 6px;
                text-align: center;
            }
        """)
        controls_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(controls_title)

        # Scroll area for controls
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea QWidget {
                background: transparent;
            }
        """)

        # Container for scrollable controls
        controls_container = QWidget()
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(8)
        controls_container.setLayout(controls_layout)

        # Connection and Arming controls
        connection_layout = QHBoxLayout()
        connection_layout.setSpacing(5)
        self.connector = Connector(self, connect_func=self.connect_vehicle)
        self.armer = Armer(self, arm_func=self.siha.arm_vehicle, disarm_func=self.siha.disarm_vehicle)
        connection_layout.addWidget(self.connector)
        connection_layout.addWidget(self.armer)
        controls_layout.addLayout(connection_layout)

        # Mode selector
        self.modSelector = ModSelector(self.siha)
        controls_layout.addWidget(self.modSelector)

        # Maneuver controls
        maneuver_section = QWidget()
        maneuver_layout = QVBoxLayout()
        maneuver_layout.setContentsMargins(0, 0, 0, 0)
        maneuver_layout.setSpacing(5)

        maneuver_title = QLabel("⚡ Manevra Kontrolleri")
        maneuver_title.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: black;
                padding: 3px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 3px;
            }
        """)
        maneuver_layout.addWidget(maneuver_title)

        # Escape maneuvers
        self.kacis_manevra = KacisManevra(sag_kacis_func=self.sag_kacis, sol_kacis_func=self.sol_kacis)
        maneuver_layout.addWidget(self.kacis_manevra)

        # Speed and altitude controls
        speed_alt_layout = QHBoxLayout()
        speed_alt_layout.setSpacing(5)
        self.hiz_gonder_wid = HizGonder(hiz_gonder_func=self.hiz_gonder)
        self.yuksel_wid = Yuksel(yuksel_func=self.yuksel)
        speed_alt_layout.addWidget(self.hiz_gonder_wid)
        speed_alt_layout.addWidget(self.yuksel_wid)
        maneuver_layout.addLayout(speed_alt_layout)

        maneuver_section.setLayout(maneuver_layout)
        controls_layout.addWidget(maneuver_section)

        # Autonomous controls
        self.otonom_ui = Otonom_UI(otonom_inis_func=self.otonom_inis, otonom_kalkis_func=self.otonom_kalkis, kamikaze_func=self.kamikaze_modu)
        controls_layout.addWidget(self.otonom_ui)

        # Add stretch to push everything up
        controls_layout.addStretch()

        scroll_area.setWidget(controls_container)
        layout.addWidget(scroll_area)

        # Connect refresh button
        self.connector.refresh_button.clicked.connect(self.refresh_telemetry)

        return panel
    
    def connect_vehicle(self, port, baudrate):
        print(f"🔌 SIHA'ya bağlanmaya çalışılıyor... Port: {port}, Baudrate: {baudrate}")
        if self.siha.connect_to_vehicle(port, baudrate):
            print(f"✅ SIHA'ya başarıyla bağlandı! Port: {port}")
            self.refresh_telemetry()
            # Restart timer with connected state
            if hasattr(self, 'telemetry_timer'):
                self.telemetry_timer.start(1000)
            return True
        else:
            print(f"❌ SIHA bağlantısı başarısız! Port: {port}")
            # Stop timer if connection fails
            if hasattr(self, 'telemetry_timer'):
                self.telemetry_timer.stop()
            return False

    def refresh_telemetry(self):
        print("📡 Telemetri verileri yenileniyor...")
        try:
            if self.siha.mavlink_connection is not None:
                self.siha.update_telemetry()
                telemetry_data = self.siha.return_telemetry_var()
                self.info_bar.update_info(telemetry_data)

                # Update map position if location data is available
                if hasattr(telemetry_data, 'get') and 'current_location' in telemetry_data:
                    location = telemetry_data['current_location']
                    if location and 'lat' in location and 'lon' in location:
                        lat = location['lat']
                        lon = location['lon']
                        if lat != 0 and lon != 0:  # Only update if we have valid coordinates
                            print(".4f")
                            self.map_widget.update_position(lat, lon)
        except Exception as e:
            print(f"Telemetri yenileme hatası: {e}")

    def sag_kacis(self):
        print(" Sağ kaçış manevrası başlatıldı!")
        
    def sol_kacis(self):
        print(" Sol kaçış manevrası başlatıldı!")

    def hiz_gonder(self, hiz):
        print(f" Hız komutu gönderildi: {hiz} m/s")
        
    def yuksel(self, yukseklik):
        print(f" Yükseklik komutu gönderildi: {yukseklik} m")
        
    def otonom_inis(self):
        print(" Otonom iniş modu aktif!")
        
    def otonom_kalkis(self):
        print(" Otonom kalkış modu aktif!")
        
    def kamikaze_modu(self):
        print(" Kamikaze modu aktif! Tehlikeli!")
        
    def start_telemetry_timer(self):
        """Start periodic telemetry updates"""
        self.telemetry_timer = QTimer()
        self.telemetry_timer.timeout.connect(self.update_infos)
        # Only start if we have a connection, otherwise just create the timer
        if self.siha.mavlink_connection is not None:
            self.telemetry_timer.start(100)  # Update every 1 second
        else:
            print("⏸️ Telemetri timer hazır - bağlantı bekleniyor...")
        
    def update_infos(self):
        """Periodic telemetry update function"""
        try:
            # Only update if we have an active connection
            if self.siha.mavlink_connection is not None:
                self.siha.update_telemetry()
                telemetry_data = self.siha.return_telemetry_var()
                self.info_bar.update_info(telemetry_data)

                # Update map position if location data is available
                if hasattr(telemetry_data, 'get') and 'current_location' in telemetry_data:
                    location = telemetry_data['current_location']
                    if location and 'lat' in location and 'lon' in location:
                        lat = location['lat']
                        lon = location['lon']
                        if lat != 0 and lon != 0:  # Only update if we have valid coordinates
                            self.map_widget.update_position(lat, lon)
                
            else:
                # No active connection, just update the info bar with empty data
                empty_data = {
                    'current_location': {'lat': 0, 'lon': 0, 'alt': 0},
                    'current_attitude': {'roll': 0, 'pitch': 0, 'yaw': 0},
                    'current_velocity': {'vx': 0, 'vy': 0, 'vz': 0},
                    'battery_info': {'voltage': 0, 'current': 0, 'remaining': 0},
                    'gps_info': {'fix_type': 0, 'satellites': 0}
                }
                self.info_bar.update_info(empty_data)
        except Exception as e:
            print(f"Telemetri güncelleme hatası: {e}")
            # Don't spam the console, wait a bit before next attempt
            import time
            time.sleep(0.1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

