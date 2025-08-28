
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox
)
from PyQt5.QtCore import Qt
from ui.styles import button_style, secondary_button_style


class KacisManevra(QWidget):
    def __init__(self, sag_kacis_func, sol_kacis_func):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Group box for maneuvers
        group_box = QGroupBox("Kaçış Manevraları")
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #8b2635;
                border-radius: 10px;
                margin-top: 15px;
                background-color: #f8f9fa;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: #8b2635;
                color: white;
                border-radius: 5px;
            }
        """)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(15, 20, 15, 15)

        # Left escape button
        sol_button = QPushButton("⬅️ Sol Kaçış")
        sol_button.setStyleSheet("""
            QPushButton {
                background-color: #8b2635;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 25px;
                min-width: 150px;
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
        sol_button.clicked.connect(sol_kacis_func)
        button_layout.addWidget(sol_button)

        # Right escape button
        sag_button = QPushButton("Sağ Kaçış ➡️")
        sag_button.setStyleSheet("""
            QPushButton {
                background-color: #8b2635;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 25px;
                min-width: 150px;
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
        sag_button.clicked.connect(sag_kacis_func)
        button_layout.addWidget(sag_button)

        group_box.setLayout(button_layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)
        
        
        