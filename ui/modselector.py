from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QWidget, QGroupBox
from ui.styles import button_style, baslik_style, secondary_button_style

class ModSelector(QWidget):
    def __init__(self, mavlink_connection=None):
        super().__init__()
        self.mavlink_connection = mavlink_connection

        # Main layout with group box for better organization
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Group box for mode selection
        group_box = QGroupBox("Flight Mode Selection")
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

        layout = QVBoxLayout()
        layout.setSpacing(12)

        self.current_mode = QLabel("Current Mode: UNKNOWN")
        self.current_mode.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1f2c51;
                padding: 8px 12px;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                border: 2px solid #1f2c51;
            }
        """)
        layout.addWidget(self.current_mode)

        # Mode buttons with better styling
        self.mode_manual = QPushButton("MANUAL")
        self.mode_stabilize = QPushButton("STABILIZE")
        self.mode_fbwa = QPushButton("FBWA")
        self.mode_loiter = QPushButton("LOITER")
        self.mode_guided = QPushButton("GUIDED")
        self.mode_auto = QPushButton("AUTO")

        # Apply different styles for different mode types
        self.mode_manual.setStyleSheet(button_style)
        self.mode_stabilize.setStyleSheet(secondary_button_style)
        self.mode_fbwa.setStyleSheet(secondary_button_style)
        self.mode_loiter.setStyleSheet(button_style)
        self.mode_guided.setStyleSheet(button_style)
        self.mode_auto.setStyleSheet(button_style)

        if mavlink_connection:
            self.mode_manual.pressed.connect(lambda: self.update_mode("MANUAL"))
            self.mode_stabilize.pressed.connect(lambda: self.update_mode("STABILIZE"))
            self.mode_fbwa.pressed.connect(lambda: self.update_mode("FBWA"))
            self.mode_loiter.pressed.connect(lambda: self.update_mode("LOITER"))
            self.mode_guided.pressed.connect(lambda: self.update_mode("GUIDED"))
            self.mode_auto.pressed.connect(lambda: self.update_mode("AUTO"))

        # Organize buttons in two rows
        layout_up = QHBoxLayout()
        layout_up.setSpacing(10)
        layout_down = QHBoxLayout()
        layout_down.setSpacing(10)

        layout_up.addWidget(self.mode_manual)
        layout_up.addWidget(self.mode_stabilize)
        layout_up.addWidget(self.mode_fbwa)

        layout_down.addWidget(self.mode_loiter)
        layout_down.addWidget(self.mode_guided)
        layout_down.addWidget(self.mode_auto)

        layout.addLayout(layout_up)
        layout.addLayout(layout_down)
        layout.addStretch()

        group_box.setLayout(layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)


    def update_mode(self, mode):
        self.mavlink_connection.set_mode(mode)
        self.current_mode.setText(f"Current Mode: {mode}")
        print(f"Mode changed to {mode}")
