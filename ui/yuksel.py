from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QTextEdit, QGroupBox

class Yuksel(QWidget):
    def __init__(self, yuksel_func=None):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Group box for altitude control
        group_box = QGroupBox("Yükseklik Kontrolü")
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #9b59b6;
                border-radius: 10px;
                margin-top: 15px;
                background-color: #f8f9fa;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: #9b59b6;
                color: white;
                border-radius: 5px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 20, 15, 15)
        layout.setSpacing(12)

        # Input field with better styling
        self.deger_textedit = QTextEdit()
        self.deger_textedit.setPlaceholderText("Yükseklik Değerini Girin (örn: 50)")
        self.deger_textedit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #9b59b6;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                background-color: #ffffff;
                selection-background-color: #9b59b6;
                min-height: 60px;
            }
            QTextEdit:focus {
                border-color: #9b59b6;
                box-shadow: 0 0 0 3px rgba(155, 89, 182, 0.2);
            }
        """)
        layout.addWidget(self.deger_textedit)

        # Send button with enhanced styling
        self.gonder_button = QPushButton("📈 Yükseklik Gönder")
        self.gonder_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 25px;
                min-width: 180px;
                min-height: 50px;
                box-shadow: 0 4px 12px rgba(155, 89, 182, 0.3);
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #8e44ad;
                box-shadow: 0 6px 16px rgba(155, 89, 182, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: #7d3c98;
                box-shadow: 0 2px 8px rgba(155, 89, 182, 0.3);
                transform: translateY(0px);
            }
        """)
        self.gonder_button.clicked.connect(lambda: yuksel_func(float(self.deger_textedit.toPlainText()) if self.deger_textedit.toPlainText() else 0))
        layout.addWidget(self.gonder_button)

        group_box.setLayout(layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)
