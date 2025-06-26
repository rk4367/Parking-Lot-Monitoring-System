# ParkVision - AI-Powered Parking Management System

## 🚗 Overview
ParkVision is an intelligent parking management system that uses computer vision and AI to monitor parking spaces in real-time. The system can detect occupied and available parking spots, provide live video feeds, and offer a web-based dashboard for monitoring multiple parking lots.

## ✨ Features
- **Real-time Parking Detection**: AI-powered spot occupancy detection
- **Live Video Streaming**: Real-time video feeds from parking lots
- **Web Dashboard**: Intuitive web interface for monitoring
- **Multi-lot Support**: Monitor multiple parking areas simultaneously
- **Historical Data**: Track parking patterns over time
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Technologies Used
- **Backend**: Python, Flask, OpenCV
- **Frontend**: HTML5, CSS3, JavaScript
- **Computer Vision**: OpenCV, NumPy
- **Real-time Processing**: Threading, Video Streaming
- **Web Technologies**: MJPEG Streaming, REST API

## 📋 Prerequisites
- Python 3.7+
- Webcam or IP camera access
- Modern web browser

## 🚀 Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/parkvision-ai-powered-parking-management.git
   cd parkvision-ai-powered-parking-management
```

## Troubleshooting Static File Issues

- Always run the app using `python app.py` and access it via `http://localhost:5000`.
- Do NOT open HTML files directly in your browser; static files will not load.
- If CSS or JS is not loading, open your browser's developer tools (F12), go to the Network tab, and look for 404 errors for `.css` or `.js` files.
- If you see 404s, ensure the `static/` folder exists and contains the correct files.
- If running in production (e.g., with gunicorn or nginx), ensure your server is configured to serve the `static/` directory.
- You can test static file serving by visiting `/static-test` in your browser.