# 🚁 Teknofest 2025 - SİHA Yer İstasyonu

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Teknofest](https://img.shields.io/badge/Teknofest-2025-FF0000?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

*UAV Ground Station System for Teknofest 2025 Autonomous Flight Competition*

[🎯 Overview](#-overview) • [✨ Features](#-features) • [🚀 Quick Start](#-quick-start) • [📚 Documentation](#-documentation)

</div>

---

## 🎯 Overview

Ground station control system developed for Teknofest 2025 Autonomous UAV (SİHA) competition. The system provides real-time telemetry monitoring, autonomous mission planning, and video streaming capabilities for unmanned aerial vehicles.

### Competition Details
- **Event**: Teknofest 2025
- **Category**: Autonomous UAV Competition
- **Mission**: Autonomous flight, object detection, and mission execution
- **Team**: [Your Team Name]

## ✨ Features

### 📊 Ground Control Station
- **Real-time Telemetry**: GPS, altitude, speed, battery monitoring
- **Live Video Feed**: HD video streaming from UAV camera
- **Mission Planning**: Waypoint creation and route planning
- **Flight Control**: Manual override and autonomous mode switching
- **Data Logging**: Complete flight data recording

### 🎯 Mission Capabilities
- **Autonomous Navigation**: GPS-based waypoint navigation
- **Object Detection**: Computer vision for target identification
- **Payload Control**: Servo and mechanism control
- **Emergency Procedures**: Auto-return and failsafe systems
- **Communication**: MAVLink protocol support

### 📹 Computer Vision
- **Target Detection**: Real-time object recognition
- **Image Processing**: OpenCV-based analysis
- **QR Code Reading**: Mission parameter extraction
- **Landing Assistance**: Visual landing guidance

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **OpenCV 4.0+**
- **MAVLink library**
- **Ground station hardware** (laptop, radio telemetry)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ernakkc/Teknofest-2025-SIHA-Yer-Istasyonu.git
   cd Teknofest-2025-SIHA-Yer-Istasyonu
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure connection**:
   ```bash
   # Edit config.yaml with your telemetry settings
   nano config.yaml
   ```

4. **Run ground station**:
   ```bash
   python main.py
   ```

## 💻 System Architecture

```
┌───────────────────┐
│   UAV (SİHA)      │
│                    │
│  - Autopilot       │
│  - Camera          │
│  - Telemetry       │
└─────────┬──────────┘
         │
         │ (Radio Telemetry)
         │
┌────────┴──────────┐
│  Ground Station   │
│                    │
│  - Telemetry GUI  │
│  - Mission Planner│
│  - Video Display  │
│  - Data Logger    │
└────────────────────┘
```

## 📁 Project Structure

```
Teknofest-2025-SIHA-Yer-Istasyonu/
├── main.py                    # Main ground station app
├── config.yaml               # Configuration file
├── requirements.txt          # Dependencies
├── src/
│   ├── gui/                  # GUI modules
│   │   ├── telemetry_panel.py
│   │   ├── video_panel.py
│   │   └── mission_panel.py
│   ├── communication/        # MAVLink communication
│   │   ├── mavlink_handler.py
│   │   └── telemetry.py
│   ├── vision/               # Computer vision
│   │   ├── object_detector.py
│   │   ├── qr_reader.py
│   │   └── landing_assist.py
│   ├── mission/              # Mission planning
│   │   ├── waypoint_manager.py
│   │   └── route_planner.py
│   └── utils/                # Utilities
│       ├── logger.py
│       └── config_loader.py
├── tests/                    # Unit tests
├── docs/                     # Documentation
└── logs/                     # Flight logs
```

## 🛠️ Technologies

### Core Technologies
- **Python 3.8+** - Main programming language
- **PyQt5/Tkinter** - GUI framework
- **OpenCV** - Computer vision
- **MAVLink** - Communication protocol
- **NumPy** - Numerical operations

### Hardware Requirements
- Laptop/PC (Windows/Linux)
- Radio telemetry module (433MHz/915MHz)
- USB connection for telemetry
- Optional: Joystick controller

## 📚 Documentation

### Configuration

```yaml
# config.yaml
connection:
  port: COM3              # Telemetry port
  baudrate: 57600
  timeout: 1

mission:
  home_altitude: 50       # meters
  max_altitude: 120       # meters
  cruise_speed: 15        # m/s

vision:
  camera_resolution: [1920, 1080]
  detection_threshold: 0.75
  model_path: "models/yolov5s.pt"

logging:
  enabled: true
  log_directory: "logs/"
  video_recording: true
```

### MAVLink Communication

```python
from src.communication.mavlink_handler import MAVLinkHandler

# Initialize connection
mavlink = MAVLinkHandler(port='COM3', baudrate=57600)
mavlink.connect()

# Get telemetry data
telemetry = mavlink.get_telemetry()
print(f"Altitude: {telemetry.altitude}m")
print(f"GPS: {telemetry.lat}, {telemetry.lon}")
```

### Object Detection

```python
from src.vision.object_detector import ObjectDetector

# Initialize detector
detector = ObjectDetector(model_path="models/yolov5s.pt")

# Detect objects in frame
detections = detector.detect(frame)
for det in detections:
    print(f"Object: {det.label}, Confidence: {det.confidence}")
```

## 🎯 Competition Requirements

### Mission Tasks
1. ✅ Autonomous takeoff
2. ✅ Navigate to waypoints
3. ✅ Detect and identify targets
4. ✅ Read QR codes for mission parameters
5. ✅ Payload delivery
6. ✅ Autonomous landing

### Scoring Criteria
- Successful autonomous flight: 40 points
- Target detection accuracy: 30 points
- Mission time: 20 points
- Landing precision: 10 points

## 🐛 Troubleshooting

### Connection Issues
```bash
# Check COM port
python -m serial.tools.list_ports

# Test MAVLink connection
python tests/test_connection.py
```

### Video Lag
```yaml
# Reduce resolution in config.yaml
camera_resolution: [1280, 720]
frame_rate: 15
```

### Object Detection Slow
```python
# Use lighter model
model_path: "models/yolov5n.pt"  # nano version
```

## 🔐 Safety

### Pre-flight Checks
- ✅ Ground station connection stable
- ✅ GPS lock acquired
- ✅ Battery level sufficient
- ✅ Emergency procedures tested
- ✅ Failsafe configured

### Emergency Procedures
- **RC Override**: Manual control takeover
- **Return to Home**: Automatic return on signal loss
- **Emergency Landing**: Immediate landing command

## 🤝 Contributing

Team members can contribute by:
1. Testing hardware integration
2. Improving computer vision algorithms
3. Optimizing flight performance
4. Documenting procedures

## 📝 License

This project is licensed under the MIT License.

## 👥 Team

**[Your Team Name]**
- Team Leader: [Name]
- Software: Eren Akkoç & Team
- Hardware: [Name]
- Vision: [Name]

**Contact**:
- 🌐 GitHub: [@ernakkc](https://github.com/ernakkc)
- 📧 Email: ern.akkc@gmail.com

---

<div align="center">

**🚁 Teknofest 2025 - SİHA Yarışması 🇹🇷**

*Autonomous Flight | Computer Vision | Mission Control*

**Good luck to all teams! 🌟**

</div> 
