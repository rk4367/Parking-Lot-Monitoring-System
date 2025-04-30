# app.py
from flask import Flask, jsonify, render_template, Response, request
import cv2
import numpy as np  # Add this import for np
import pickle
import threading
import time
import os
from pathlib import Path
from test3 import ParkingMonitor

app = Flask(__name__, static_folder="static", template_folder="templates")

# Global variables to store parking data
parking_data = {
    'lot1': {'total': 0, 'available': 0, 'occupied': 0, 'history': []},
    'lot2': {'total': 0, 'available': 0, 'occupied': 0, 'history': []}
}

# Create frames to store the latest processed frames for streaming
frames = {
    '1': None,
    '2': None
}

# Function to update parking data in background
def update_parking_data():
    monitor = ParkingMonitor()
    
    # Load positions for both lots
    for i in range(2):
        pos_file = monitor.pos_files[i]
        lot_key = f'lot{i+1}'
        
        try:
            if pos_file.exists():
                with open(pos_file, 'rb') as f:
                    positions = pickle.load(f)
                    parking_data[lot_key]['total'] = len(positions)
        except Exception as e:
            print(f"Error loading positions for lot {i+1}: {e}")
    
    # Initialize video captures
    caps = []
    positions_list = []
    
    for i in range(2):
        video_path = monitor.video_paths[i]
        pos_file = monitor.pos_files[i]
        
        try:
            if pos_file.exists():
                with open(pos_file, 'rb') as f:
                    positions = pickle.load(f)
                    positions_list.append(positions)
                
                cap = cv2.VideoCapture(str(video_path))
                if not cap.isOpened():
                    caps.append(None)
                    print(f"Failed to open video {i+1}")
                else:
                    caps.append(cap)
            else:
                caps.append(None)
                positions_list.append([])
                print(f"No positions file for lot {i+1}")
        except Exception as e:
            print(f"Error setting up video {i+1}: {e}")
            caps.append(None)
            positions_list.append([])
    
    # Process frames and update data continuously
    while True:
        for i, (cap, positions) in enumerate(zip(caps, positions_list)):
            lot_key = f'lot{i+1}'
            lot_idx = str(i+1)
            
            if cap is None or not positions:
                continue
            
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # Process the frame
            processed_frame = monitor.process_frame(frame.copy(), positions, i)
            
            # Count free spots
            free_count = 0
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 1)
            thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 25, 16)
            processed = cv2.medianBlur(thresh, 5)
            kernel = np.ones((3, 3), np.uint8)
            processed = cv2.dilate(processed, kernel, iterations=1)
            
            for x, y, w, h in positions:
                spot = processed[y:y+h, x:x+w]
                nonzero = cv2.countNonZero(spot)
                
                if nonzero <= (w * h * monitor.OCCUPANCY_THRESHOLD):
                    free_count += 1
            
            # Update parking data
            occupied_count = len(positions) - free_count
            
            parking_data[lot_key]['available'] = free_count
            parking_data[lot_key]['occupied'] = occupied_count
            
            # Add to history (max 50 entries)
            now = time.strftime("%H:%M:%S")
            history_entry = {
                'time': now,
                'available': free_count,
                'occupied': occupied_count
            }
            
            parking_data[lot_key]['history'].append(history_entry)
            if len(parking_data[lot_key]['history']) > 50:
                parking_data[lot_key]['history'] = parking_data[lot_key]['history'][-50:]
            
            # Store processed frame for streaming
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            if ret:
                frames[lot_idx] = buffer.tobytes()
        
        # Sleep to avoid high CPU usage
        time.sleep(0.1)

# Function to generate streaming response
def generate_frames(lot_id):
    while True:
        if frames[lot_id] is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frames[lot_id] + b'\r\n')
        else:
            # If no frame is available, return a blank frame
            blank_frame = np.zeros((480, 640, 3), np.uint8)
            blank_frame = cv2.putText(blank_frame, "No video feed available", (150, 240),
                                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            _, buffer = cv2.imencode('.jpg', blank_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/details.html')
def details():
    return render_template('details.html')

@app.route('/api/parking-data')
def get_parking_data():
    return jsonify({
        'lot1': {
            'total': parking_data['lot1']['total'],
            'available': parking_data['lot1']['available'],
            'occupied': parking_data['lot1']['occupied']
        },
        'lot2': {
            'total': parking_data['lot2']['total'],
            'available': parking_data['lot2']['available'],
            'occupied': parking_data['lot2']['occupied']
        }
    })

@app.route('/api/parking-details')
def get_parking_details():
    lot = request.args.get('lot', '1')
    lot_key = f'lot{lot}'
    
    if lot_key in parking_data:
        return jsonify({
            'total': parking_data[lot_key]['total'],
            'available': parking_data[lot_key]['available'],
            'occupied': parking_data[lot_key]['occupied'],
            'history': parking_data[lot_key]['history']
        })
    else:
        return jsonify({'error': 'Invalid lot number'}), 400

@app.route('/api/video-stream')
def video_stream():
    lot = request.args.get('lot', '1')
    if lot not in ['1', '2']:
        return "Invalid lot number", 400
    
    return Response(generate_frames(lot),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start background thread to update parking data
    thread = threading.Thread(target=update_parking_data)
    thread.daemon = True
    thread.start()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)