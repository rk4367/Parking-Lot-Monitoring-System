# ParkVision - AI-Powered Parking Management System

## 🚗 Overview

ParkVision is an intelligent parking management system that leverages computer vision and AI to monitor parking spaces in real-time. The system automatically detects occupied and available parking spots, provides live video feeds, and offers a comprehensive web-based dashboard for monitoring multiple parking lots simultaneously.

## ✨ Features

### Core Functionality
- **🎯 Real-time Parking Detection**: Advanced computer vision algorithms for accurate spot occupancy detection
- **📹 Live Video Streaming**: Real-time MJPEG video feeds from multiple parking lots
- **🌐 Web Dashboard**: Intuitive, responsive web interface for monitoring and management
- **🏢 Multi-lot Support**: Simultaneous monitoring of multiple parking areas
- **📊 Historical Analytics**: Track parking patterns and occupancy trends over time
- **📱 Mobile Responsive**: Works seamlessly on desktop, tablet, and mobile devices

### Technical Features
- **⚡ High Performance**: Optimized frame processing with threading and queue management
- **🔄 Auto-recovery**: Automatic video stream retry mechanisms and error handling
- **⚙️ Configurable**: Interactive parking spot configuration system
- **🔧 RESTful API**: Clean API endpoints for data integration
- **🎨 Modern UI**: Contemporary design with smooth animations and transitions

## 🛠️ Technologies Used

### Backend
- **Python 3.7+**: Core programming language
- **Flask 2.3.3**: Web framework for API and routing
- **OpenCV 4.8.1**: Computer vision and image processing
- **NumPy 1.24.3**: Numerical computing for image analysis
- **Threading**: Concurrent processing for real-time performance

### Frontend
- **HTML5 & CSS3**: Modern web standards
- **JavaScript (ES6+)**: Dynamic user interactions
- **Font Awesome**: Professional iconography
- **Responsive Design**: Mobile-first approach

### Computer Vision Pipeline
- **Adaptive Thresholding**: Dynamic lighting condition handling
- **Gaussian Blur**: Noise reduction
- **Morphological Operations**: Image enhancement
- **Occupancy Detection**: Pixel-based vacancy analysis

## 📋 Prerequisites

- **Python 3.7 or higher**
- **Webcam or IP camera access**
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Video files** for parking lot monitoring (MP4 format recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/parkvision-ai-powered-parking-management.git
cd parkvision-ai-powered-parking-management
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Project Structure Setup
Ensure your project structure matches:
```
parkvision/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── assets/               # Video files and coordinates
│   ├── video-1.mp4
│   ├── video-3.mp4
│   ├── coordinate-video-1
│   └── coordinate-video-3
├── core/
│   └── parking_monitor.py # Core computer vision logic
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── script.js
│       └── details.js
└── templates/
    ├── index.html
    └── details.html
```

### 5. Configure Parking Spots
```bash
# Run the parking monitor to configure spots
python core/parking_monitor.py
```

**Configuration Controls:**
- **Left Click**: Add new parking spot
- **Left Drag**: Resize existing spot
- **Right Click**: Delete spot
- **'R' Key**: Reset all spots
- **ESC**: Save and exit

### 6. Launch the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your web browser.

## 📖 Usage Guide

### Initial Setup
1. **Video Configuration**: Place your parking lot video files in the `assets/` directory
2. **Spot Configuration**: Run the configuration tool to mark parking spaces
3. **Launch Dashboard**: Start the Flask application and access the web interface

### Web Interface
- **Main Dashboard**: Overview of all parking lots with real-time statistics
- **Details View**: Individual lot monitoring with live video feed
- **Real-time Updates**: Automatic data refresh every 3-5 seconds

### API Endpoints
- `GET /api/parking-data`: Retrieve current parking statistics
- `GET /api/parking-details?lot=1`: Get detailed information for specific lot
- `GET /api/video-stream?lot=1`: Access live video stream

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Video Input   │───▶│  Computer Vision │───▶│   Web Dashboard │
│   (Cameras/     │    │   Processing     │    │   (Flask App)   │
│    Files)       │    │   (OpenCV)       │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Real-time Data  │
                       │   Processing     │
                       │  (Threading)     │
                       └──────────────────┘
```

## ⚙️ Configuration Options

### Video Settings
```python
# Frame processing optimization
FRAME_SKIP = 1              # Process every nth frame
OCCUPANCY_THRESHOLD = 0.2   # Sensitivity for spot detection
```

### Parking Spot Dimensions
```python
SPOT_WIDTH = 90   # Default spot width in pixels
SPOT_HEIGHT = 30  # Default spot height in pixels
```

## 🔧 Troubleshooting

### Common Issues

**Static Files Not Loading**
- Ensure you're accessing via `http://localhost:5000`, not opening HTML files directly
- Check browser developer tools (F12) for 404 errors
- Verify `static/` folder structure

**Video Stream Issues**
- Check video file paths in `parking_monitor.py`
- Ensure video files are in correct format (MP4 recommended)
- Verify camera permissions if using live cameras

**Performance Issues**
- Adjust `FRAME_SKIP` value to process fewer frames
- Reduce video resolution if needed
- Check system resources (CPU/Memory usage)

**Configuration Problems**
- Delete coordinate files to reconfigure spots
- Ensure video files are accessible
- Check file permissions

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test thoroughly before submitting
- Update documentation as needed

## 🎯 Future Enhancements

- [ ] **Database Integration**: Persistent data storage with SQLite/PostgreSQL
- [ ] **Machine Learning**: Advanced occupancy prediction algorithms
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **Cloud Integration**: AWS/Azure deployment capabilities
- [ ] **Analytics Dashboard**: Advanced reporting and insights
- [ ] **Alert System**: Email/SMS notifications for parking events
- [ ] **Payment Integration**: Parking fee management system
- [ ] **Multi-camera Support**: Enhanced camera management
- [ ] **Night Vision**: Low-light condition optimization
- [ ] **Weather Adaptation**: Environmental condition handling

## 🙏 Acknowledgments

- **OpenCV Community**: For excellent computer vision libraries
- **Flask Team**: For the lightweight web framework
- **Contributors**: Thanks to all contributors and testers
</div>
