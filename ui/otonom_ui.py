from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QGroupBox
from ui.styles import button_style, baslik_style, danger_button_style

class Otonom_UI(QWidget):
    def __init__(self, otonom_inis_func=None, otonom_kalkis_func=None, kamikaze_func=None):
        super().__init__()

        self.otonom_inis_func = otonom_inis_func
        self.otonom_kalkis_func = otonom_kalkis_func
        self.kamikaze_func = kamikaze_func

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Group box for autonomous controls
        group_box = QGroupBox("Otonom Kontrol Paneli")
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #34495e;
                border-radius: 10px;
                margin-top: 15px;
                background-color: #f8f9fa;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: #34495e;
                color: white;
                border-radius: 5px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 20, 15, 15)
        layout.setSpacing(15)

        # Autonomous takeoff and landing buttons
        alt_layout = QHBoxLayout()
        alt_layout.setSpacing(15)

        otonom_inis = QPushButton("⬇️ Otonom İniş")
        otonom_inis.setStyleSheet("""
            QPushButton {
                background-color: #8b2635;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 20px;
                min-width: 140px;
                min-height: 50px;
                box-shadow: 0 4px 12px rgba(139, 38, 53, 0.3);
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #a93226;
                box-shadow: 0 6px 16px rgba(139, 38, 53, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: #6c1e1e;
                box-shadow: 0 2px 8px rgba(139, 38, 53, 0.3);
                transform: translateY(0px);
            }
        """)
        otonom_inis.clicked.connect(self.otonom_inis_func)
        alt_layout.addWidget(otonom_inis)

        otonom_kalkis = QPushButton("⬆️ Otonom Kalkış")
        otonom_kalkis.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 20px;
                min-width: 140px;
                min-height: 50px;
                box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #229954;
                box-shadow: 0 6px 16px rgba(39, 174, 96, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: #1e8449;
                box-shadow: 0 2px 8px rgba(39, 174, 96, 0.3);
                transform: translateY(0px);
            }
        """)
        otonom_kalkis.clicked.connect(self.otonom_kalkis_func)
        alt_layout.addWidget(otonom_kalkis)

        layout.addLayout(alt_layout)

        # Kamikaze button with danger styling
        kamikaze_button = QPushButton("💀 Kamikaze Modu")
        kamikaze_button.setStyleSheet("""
            QPushButton {
                background-color: #8b2635;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 25px;
                min-width: 180px;
                min-height: 50px;
                box-shadow: 0 4px 12px rgba(139, 0, 0, 0.4);
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #a93226;
                box-shadow: 0 6px 16px rgba(139, 38, 53, 0.5);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: #6c1e1e;
                box-shadow: 0 2px 8px rgba(139, 38, 53, 0.3);
                transform: translateY(0px);
            }
        """)
        kamikaze_button.clicked.connect(self.kamikaze_func)
        layout.addWidget(kamikaze_button)

        group_box.setLayout(layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

        