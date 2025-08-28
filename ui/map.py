from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
from PyQt5.QtCore import Qt

class MapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

        # Group box for map
        group_box = QGroupBox("Harita Görünümü")
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #1f2c51;
                border-radius: 8px;
                margin-top: 12px;
                background-color: rgba(255, 255, 255, 0.95);
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 8px 0 8px;
                background-color: #1f2c51;
                color: white;
                border-radius: 4px;
            }
        """)

        inner_layout = QVBoxLayout()
        inner_layout.setContentsMargins(10, 15, 10, 10)
        inner_layout.setSpacing(8)

        # WebEngineView for map
        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(400, 300)
        self.web_view.setHtml(self.html_template())

        inner_layout.addWidget(self.web_view)
        group_box.setLayout(inner_layout)
        main_layout.addWidget(group_box)

    def html_template(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>SİHA Map</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <style>
                #map { height: 100vh; width: 100vw; }
                body { margin: 0; padding: 0; }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                var map = L.map('map').setView([41.0082, 28.9784], 13); // default İstanbul
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);

                // UAV marker
                var uavMarker = L.marker([41.0082, 28.9784]).addTo(map).bindPopup("🚁 SİHA");

                function updateUAV(lat, lon) {
                    uavMarker.setLatLng([lat, lon]);
                    map.panTo([lat, lon]);  // haritayı takip ettir
                }
            </script>
        </body>
        </html>
        """

    def update_position(self, lat, lon):
        js = f"updateUAV({lat}, {lon});"
        self.web_view.page().runJavaScript(js)
