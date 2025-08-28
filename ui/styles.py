button_style = """
QPushButton {
    background-color: #1f2c51;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    font-size: 12px;
    padding: 8px 16px;
    min-width: 80px;
    min-height: 32px;
    box-shadow: 0 2px 6px rgba(31, 44, 81, 0.3);
    transition: all 0.3s ease;
}
QPushButton:hover {
    background-color: #2c3e50;
    box-shadow: 0 3px 8px rgba(31, 44, 81, 0.4);
    transform: translateY(-1px);
}
QPushButton:pressed {
    background-color: #141a2e;
    box-shadow: 0 1px 3px rgba(31, 44, 81, 0.3);
    transform: translateY(0px);
}
QPushButton:disabled {
    background-color: #95a5a6;
    color: #ecf0f1;
}
"""

danger_button_style = """
QPushButton {
    background-color: #8b2635;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    font-size: 12px;
    padding: 8px 16px;
    min-width: 80px;
    min-height: 32px;
    box-shadow: 0 2px 6px rgba(139, 38, 53, 0.3);
    transition: all 0.3s ease;
}
QPushButton:hover {
    background-color: #a93226;
    box-shadow: 0 3px 8px rgba(139, 38, 53, 0.4);
    transform: translateY(-1px);
}
QPushButton:pressed {
    background-color: #6c1e1e;
    box-shadow: 0 1px 3px rgba(139, 38, 53, 0.3);
    transform: translateY(0px);
}
"""

secondary_button_style = """
QPushButton {
    background-color: #2c3e50;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    font-size: 12px;
    padding: 8px 16px;
    min-width: 80px;
    min-height: 32px;
    box-shadow: 0 2px 6px rgba(44, 62, 80, 0.3);
    transition: all 0.3s ease;
}
QPushButton:hover {
    background-color: #34495e;
    box-shadow: 0 3px 8px rgba(44, 62, 80, 0.4);
    transform: translateY(-1px);
}
QPushButton:pressed {
    background-color: #1f2c51;
    box-shadow: 0 1px 3px rgba(44, 62, 80, 0.3);
    transform: translateY(0px);
}
"""

label_style = '''
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
QLabel {
    font-size: 12px;
    color: #1f2c51;
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 6px;
    padding: 6px 10px;
    margin: 3px;
    border: 1px solid #dee2e6;
    font-weight: 500;
}
'''

baslik_style = '''
QLabel {
    font-size: 18px;
    font-weight: bold;
    color: white;
    padding: 10px 15px;
    border-bottom: 3px solid #1f2c51;
    margin-bottom: 10px;
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    border-radius: 8px 8px 0 0;
}
'''

input_style = '''
QTextEdit {
    border: 2px solid #7f8c8d;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    background-color: #ffffff;
    selection-background-color: #2c3e50;
}
QTextEdit:focus {
    border-color: #2c3e50;
    box-shadow: 0 0 0 2px rgba(44, 62, 80, 0.2);
}
QLineEdit {
    border: 2px solid #7f8c8d;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
    background-color: #ffffff;
}
QLineEdit:focus {
    border-color: #2c3e50;
    box-shadow: 0 0 0 2px rgba(44, 62, 80, 0.2);
}
'''

combo_style = '''
QComboBox {
    border: 2px solid #7f8c8d;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
    background-color: #ffffff;
    min-width: 120px;
}
QComboBox:focus {
    border-color: #2c3e50;
    box-shadow: 0 0 0 2px rgba(44, 62, 80, 0.2);
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox::down-arrow {
    image: url(down_arrow.png);
    width: 12px;
    height: 12px;
}
'''

status_label_style = '''
QLabel {
    font-size: 16px;
    font-weight: bold;
    color: #27ae60;
    padding: 8px 12px;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
    border: 2px solid #27ae60;
}
'''

error_label_style = '''
QLabel {
    font-size: 16px;
    font-weight: bold;
    color: #8b2635;
    padding: 8px 12px;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
    border: 2px solid #8b2635;
}
'''

main_window_style = '''
QWidget {
    background: -webkit-linear-gradient(90deg, #1f2c51, #1f2c51, #000000);
    background: linear-gradient(90deg, #1f2c51, #1f2c51, #000000);
}
QGroupBox {
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 10px;
    margin-top: 15px;
}
'''