# ParkVision - AI-Powered Parking Management System

## 🚗 Overview
ParkVision is an intelligent parking management system that leverages computer vision and AI to monitor parking spaces in real-time. The system automatically detects occupied and available parking spots, provides live video feeds, and offers a comprehensive web-based dashboard for monitoring multiple parking lots simultaneously.

## ✨ Features

- **🎯 Real-time Parking Detection:** Advanced computer vision algorithms for accurate spot occupancy detection
- **📹 Live Video Streaming:** Real-time MJPEG video feeds from multiple parking lots
- **🌐 Web Dashboard:** Intuitive, responsive web interface for monitoring and management
- **🏢 Multi-lot Support:** Simultaneous monitoring of multiple parking areas
- **📊 Historical Analytics:** Track parking patterns and occupancy trends over time
- **📱 Mobile Responsive:** Works seamlessly on desktop, tablet, and mobile devices

## 🔧 Technical Features

- **Backend**: Python, Flask, OpenCV, NumPy
- **Frontend**: HTML, CSS, JavaScript
- **Video Processing**: OpenCV with adaptive thresholding
- **Real-time Updates**: Asynchronous JavaScript with Fetch API

## 📦 Project Structure

```
Parking_lot_detection/
│
├── app.py              # Main Flask application
├── test3.py            # Parking spot detection class
│
├── assets/             # Video files and parking spot configurations
│   ├── p1              # Parking lot 1 spot configuration
│   ├── p1.mp4          # Parking lot 1 video feed
│   ├── p2              # Parking lot 2 spot configuration
│   ├── p2.mp4          # Parking lot 2 video feed
│   ├── p3              # Parking lot 3 spot configuration
│   ├── p3.mp4          # Parking lot 3 video feed
│   └── CarParkPos4     # Additional parking configuration
│
├── static/             # Static web assets
│   ├── details.js      # JavaScript for details page
│   ├── script.js       # JavaScript for main page
│   └── styles.css      # CSS styles
│
└── templates/          # HTML templates
    ├── details.html    # Parking lot details page
    └── index.html      # Main dashboard page
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- OpenCV (cv2)
- Flask

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Parking_lot_detection.git
   cd Parking_lot_detection
   ```

2. Install the required packages:
   ```bash
   pip install flask opencv-python numpy
   ```

3. Prepare your parking lot videos:
   - Place your video feeds in the `assets/` directory
   - Videos should be named `p1.mp4`, `p2.mp4`, etc.

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the web interface:
   - Open your browser and go to `http://localhost:5000`

## 🎮 Usage

### Configure Parking Spaces

1. Run the application in configuration mode:
   ```bash
   python test3.py
   ```

2. For each parking lot video:
   - Use left-click to add parking spaces
   - Drag to resize spaces
   - Right-click to delete spaces
   - Press 'r' to reset all spaces
   - Press ESC to save and exit

### View Parking Status

1. Open the web application in your browser
2. The main dashboard shows an overview of all parking lots
3. Click "More Info" to see details for a specific lot
4. The details page includes:
   - Live video feed with space status overlay
   - Real-time statistics (total, available, occupied)
   - Automatic updates every 5 seconds

## 🛠️ How It Works

1. **Parking Space Detection**:
   - The system uses computer vision techniques to detect available parking spaces
   - Each space is processed using adaptive thresholding to determine occupancy
   - A space is considered occupied when the pixel count exceeds a configurable threshold

2. **Web Interface**:
   - Flask serves a responsive web interface
   - JavaScript handles real-time updates via API calls
   - Video feed is streamed using multipart/x-mixed-replace format

3. **Background Processing**:
   - A background thread continuously processes video frames
   - Parking statistics are updated in real-time
   - The system handles multiple parking lots simultaneously

## 🙏 Acknowledgments

- OpenCV team for the computer vision library
- Flask team for the web framework
- Font Awesome for icons

## 🔄 Future Improvements

- [ ] Add user authentication
- [ ] Implement time-based analytics
- [ ] Add email/SMS notifications when lots are full
- [ ] Improve detection accuracy with machine learning
- [ ] Add mobile app interface
