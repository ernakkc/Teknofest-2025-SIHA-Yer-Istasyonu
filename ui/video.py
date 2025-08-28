from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox


import cv2

class VideoFeed(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

        # Group box for video feed
        group_box = QGroupBox("Kamera Görüntüsü")
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

        self.label = QLabel(self)
        self.label.setFixedSize(400, 300)  # Smaller size for compact layout
        self.label.setStyleSheet("""
            QLabel {
                background-color: #1f2c51;
                border: 3px solid #2c3e50;
                border-radius: 8px;
                color: white;
                font-size: 14px;
                text-align: center;
            }
        """)
        self.label.setAlignment(Qt.AlignCenter)
        inner_layout.addWidget(self.label)
        inner_layout.setAlignment(Qt.AlignCenter)

        group_box.setLayout(inner_layout)
        main_layout.addWidget(group_box)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.label.setText("Kamera açılamadı!\nLütfen kamera bağlantınızı kontrol edin.")
            self.label.setStyleSheet("""
                QLabel {
                    background-color: #8b2635;
                    border: 3px solid #6c1e1e;
                    border-radius: 8px;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    text-align: center;
                    padding: 20px;
                }
            """)
            return

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(image))
            
    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        super().closeEvent(event)