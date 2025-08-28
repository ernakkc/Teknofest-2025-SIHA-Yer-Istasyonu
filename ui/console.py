from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QGroupBox, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime

class ConsoleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Create string buffers to capture output
        self.stdout_buffer = io.StringIO()
        self.stderr_buffer = io.StringIO()

        # Redirect stdout and stderr
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        # Start capturing output
        self.start_capture()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

        # Group box for console
        group_box = QGroupBox("Sistem Konsolu")
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #1f2c51;
                border-radius: 8px;
                margin-top: 12px;
                background-color: rgba(26, 26, 26, 0.95);
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

        # Console output area
        self.console_text = QTextEdit()
        self.console_text.setReadOnly(True)
        self.console_text.setFont(QFont("Consolas", 10))
        self.console_text.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                color: #1f2c51;
                border: 2px solid #1f2c51;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'Courier New', monospace;
                selection-background-color: #1f2c51;
                selection-color: #ffffff;
            }
        """)
        self.console_text.setMaximumHeight(200)

        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)

        self.clear_button = QPushButton("🗑️ Temizle")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #8b2635;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10px;
                padding: 6px 12px;
                min-width: 60px;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #a93226;
            }
            QPushButton:pressed {
                background-color: #6c1e1e;
            }
        """)
        self.clear_button.clicked.connect(self.clear_console)

        self.auto_scroll_button = QPushButton("📍 Otomatik Kaydır")
        self.auto_scroll_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10px;
                padding: 6px 12px;
                min-width: 100px;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.auto_scroll_button.clicked.connect(self.toggle_auto_scroll)
        self.auto_scroll_enabled = True

        self.save_button = QPushButton("💾 Kaydet")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10px;
                padding: 6px 12px;
                min-width: 60px;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #3d566e;
            }
            QPushButton:pressed {
                background-color: #2c3e50;
            }
        """)
        self.save_button.clicked.connect(self.save_logs)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.auto_scroll_button)
        button_layout.addWidget(self.save_button)
        button_layout.addStretch()

        inner_layout.addWidget(self.console_text)
        inner_layout.addLayout(button_layout)
        group_box.setLayout(inner_layout)
        main_layout.addWidget(group_box)

        # Add initial message
        self.log_message("=== SIHA Sistem Konsolu Başlatıldı ===", "info")
        self.log_message("Sistem hazır - Tüm loglar burada görüntülenecek", "success")
        self.log_message("Bağlantı, telemetri ve komut logları takip edilecek", "info")

    def start_capture(self):
        """Start capturing stdout and stderr"""
        sys.stdout = ConsoleRedirector(self, "stdout")
        sys.stderr = ConsoleRedirector(self, "stderr")

    def stop_capture(self):
        """Stop capturing and restore original stdout/stderr"""
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def log_message(self, message, level="info"):
        """Add a message to the console with appropriate color"""
        colors = {
            "info": "#00ff00",      # Green
            "warning": "#ffff00",   # Yellow
            "error": "#ff4444",     # Red
            "debug": "#8888ff",     # Blue
            "success": "#00ff88",   # Light green
        }

        color = colors.get(level, "#ffffff")
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Add level indicator
        level_indicators = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "debug": "🔍",
            "success": "✅"
        }

        indicator = level_indicators.get(level, "📝")
        formatted_message = f"[{timestamp}] {indicator} {message}\n"

        # Add colored text
        cursor = self.console_text.textCursor()
        cursor.movePosition(QTextCursor.End)

        # Set color
        char_format = cursor.charFormat()
        char_format.setForeground(Qt.black)  # Background is dark, so text should be light
        cursor.setCharFormat(char_format)

        cursor.insertText(formatted_message)

        # Auto scroll to bottom if enabled
        if self.auto_scroll_enabled:
            self.console_text.verticalScrollBar().setValue(
                self.console_text.verticalScrollBar().maximum()
            )

    def clear_console(self):
        """Clear the console"""
        self.console_text.clear()
        self.log_message("=== Konsol Temizlendi ===", "info")

    def toggle_auto_scroll(self):
        """Toggle auto scroll"""
        self.auto_scroll_enabled = not self.auto_scroll_enabled
        status = "aktif" if self.auto_scroll_enabled else "pasif"
        self.auto_scroll_button.setText(f"📍 Otomatik Kaydır ({status})")
        self.log_message(f"Otomatik kaydırma {status}", "debug")

    def save_logs(self):
        """Save console logs to a file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"siha_console_log_{timestamp}.txt"

            filename, _ = QFileDialog.getSaveFileName(
                self, "Log Dosyasını Kaydet", default_filename,
                "Text Files (*.txt);;All Files (*)"
            )

            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.console_text.toPlainText())
                self.log_message(f"Loglar kaydedildi: {filename}", "success")
        except Exception as e:
            self.log_message(f"Log kaydetme hatası: {e}", "error")

class ConsoleRedirector:
    """Redirector class to capture stdout/stderr"""

    def __init__(self, console_widget, stream_type):
        self.console_widget = console_widget
        self.stream_type = stream_type
        self.buffer = ""

    def write(self, text):
        if text.strip():  # Only log non-empty text
            level = "error" if self.stream_type == "stderr" else "info"
            self.console_widget.log_message(text.strip(), level)

    def flush(self):
        pass
