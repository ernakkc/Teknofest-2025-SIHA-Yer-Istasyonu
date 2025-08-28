from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QGroupBox


class OutputEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.output = ""

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # Group box for output console
        group_box = QGroupBox("Output Console")
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
        layout.setSpacing(10)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                border: 2px solid #34495e;
                border-radius: 10px;
                font-size: 14px;
                font-family: 'Consolas', 'Courier New', monospace;
                padding: 15px;
                color: #ecf0f1;
                selection-background-color: #3498db;
            }
        """)
        self.output_text.setMinimumHeight(200)
        layout.addWidget(self.output_text)

        group_box.setLayout(layout)
        main_layout.addWidget(group_box)

    def update_output(self, text):
        self.output_text.setPlainText(text)

    def error(self, text):
        self.append_html(f'<span style="color: #e74c3c; font-weight: bold;">[ERROR] {text}</span>')

    def warning(self, text):
        self.append_html(f'<span style="color: #f39c12; font-weight: bold;">[WARNING] {text}</span>')

    def code(self, text):
        self.append_html(f'<pre style="background:#34495e; color:#ecf0f1; border-radius:8px; padding:10px; margin:5px 0; border-left:4px solid #3498db;">{text}</pre>')

    def append_html(self, html):
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertHtml(html + "<br>")
        self.output_text.setTextCursor(cursor)