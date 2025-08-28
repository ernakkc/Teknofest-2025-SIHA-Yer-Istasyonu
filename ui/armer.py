from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QLabel, QGroupBox

class Armer(QWidget):
    def __init__(self, parent=None, arm_func=None, disarm_func=None):
        super().__init__()

        self.arm_func = arm_func
        self.disarm_func = disarm_func

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Group box for arming controls
        group_box = QGroupBox("Arming Controls")
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

        # Main layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(15, 20, 15, 15)
        button_layout.setSpacing(15)

        # Arm button with enhanced styling
        self.arm_button = QPushButton("🔓 ARM")
        self.arm_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 25px;
                min-width: 120px;
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

        # Disarm button with danger styling
        self.disarm_button = QPushButton("🔒 DISARM")
        self.disarm_button.setStyleSheet("""
            QPushButton {
                background-color: #8b2635;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 25px;
                min-width: 120px;
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

        button_layout.addWidget(self.arm_button)
        button_layout.addWidget(self.disarm_button)

        self.arm_button.clicked.connect(self.arm_func)
        self.disarm_button.clicked.connect(self.disarm_func)

        group_box.setLayout(button_layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

        