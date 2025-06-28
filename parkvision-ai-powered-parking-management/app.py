# app.py

from flask import Flask, jsonify, render_template, Response, request
import cv2
import numpy as np
import pickle
import threading
import time
import os
from pathlib import Path
from core.parking_monitor import ParkingMonitor
from queue import Queue, Empty

app = Flask(__name__, static_folder="static", template_folder="templates")

# === Global variables ===
parking_data = {
    'lot1': {'total': 0, 'available': 0, 'occupied': 0, 'history': []},
    'lot2': {'total': 0, 'available': 0, 'occupied': 0, 'history': []}
}

frame_queues = {
    '1': Queue(maxsize=5),
    '2': Queue(maxsize=5)
}

# === Background worker to update parking data ===
def update_parking_data():
    monitor = ParkingMonitor()
    
    # Load positions
    for i in range(2):
        pos_file = monitor.pos_files[i]
        lot_key = f'lot{i+1}'
        if pos_file.exists():
            try:
                with open(pos_file, 'rb') as f:
                    positions = pickle.load(f)
                    parking_data[lot_key]['total'] = len(positions)
            except Exception as e:
                print(f"[ERROR] Couldn't load positions for {lot_key}: {e}")
        else:
            print(f"[WARN] Positions file not found: {pos_file}")

    caps, positions_list = [], []

    for i in range(2):
        video_path = monitor.video_paths[i]
        pos_file = monitor.pos_files[i]
        lot_key = f'lot{i+1}'

        if not pos_file.exists():
            caps.append(None)
            positions_list.append([])
            continue

        try:
            with open(pos_file, 'rb') as f:
                positions = pickle.load(f)
                positions_list.append(positions)

            cap = cv2.VideoCapture(str(video_path))
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
                caps.append(cap)
            else:
                print(f"[ERROR] Cannot open video source: {video_path}")
                caps.append(None)
        except Exception as e:
            print(f"[ERROR] Setup failed for {lot_key}: {e}")
            caps.append(None)
            positions_list.append([])

    video_fps = [cap.get(cv2.CAP_PROP_FPS) if cap else 30 for cap in caps]

    frame_counters = [0, 0]
    last_update_time = [time.time(), time.time()]

    while True:
        for i, (cap, positions) in enumerate(zip(caps, positions_list)):
            lot_key = f'lot{i+1}'
            lot_idx = str(i+1)

            if cap is None or not positions:
                continue

            now = time.time()
            elapsed = now - last_update_time[i]
            frames_to_process = int(elapsed * video_fps[i])

            if frames_to_process > 0:
                for _ in range(frames_to_process - 1):
                    cap.grab()

                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue

                processed_frame = monitor.process_frame(frame.copy(), positions, i)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (3, 3), 1)
                thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                               cv2.THRESH_BINARY_INV, 25, 16)
                processed = cv2.medianBlur(thresh, 5)
                processed = cv2.dilate(processed, np.ones((3, 3), np.uint8), iterations=1)

                free_count = sum(
                    cv2.countNonZero(processed[y:y+h, x:x+w]) <= (w * h * monitor.OCCUPANCY_THRESHOLD)
                    for x, y, w, h in positions
                )

                occupied_count = len(positions) - free_count

                parking_data[lot_key].update({
                    'available': free_count,
                    'occupied': occupied_count
                })

                frame_counters[i] += 1
                if frame_counters[i] % 10 == 0:
                    timestamp = time.strftime("%H:%M:%S")
                    parking_data[lot_key]['history'].append({
                        'time': timestamp,
                        'available': free_count,
                        'occupied': occupied_count
                    })
                    parking_data[lot_key]['history'] = parking_data[lot_key]['history'][-50:]

                ret, buffer = cv2.imencode('.jpg', processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                if ret:
                    if frame_queues[lot_idx].full():
                        try:
                            frame_queues[lot_idx].get_nowait()
                        except Empty:
                            pass
                    frame_queues[lot_idx].put(buffer.tobytes())

                last_update_time[i] = now

# === MJPEG stream ===
def generate_frames(lot_id):
    blank_frame = np.zeros((480, 640, 3), np.uint8)
    blank_frame = cv2.putText(blank_frame, "No video feed available", (150, 240),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    _, blank_buffer = cv2.imencode('.jpg', blank_frame)
    blank_data = blank_buffer.tobytes()

    yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n')

    while True:
        try:
            frame_data = frame_queues[lot_id].get(timeout=0.5)
            yield (frame_data + b'\r\n--frame\r\nContent-Type: image/jpeg\r\n\r\n')
        except Empty:
            yield (blank_data + b'\r\n--frame\r\nContent-Type: image/jpeg\r\n\r\n')

# === Flask Routes ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/details.html')
def details():
    return render_template('details.html')

@app.route('/api/parking-data')
def get_parking_data():
    return jsonify({
        'lot1': parking_data['lot1'],
        'lot2': parking_data['lot2']
    })

@app.route('/api/parking-details')
def get_parking_details():
    lot = request.args.get('lot', '1')
    lot_key = f'lot{lot}'
    if lot_key in parking_data:
        return jsonify(parking_data[lot_key])
    return jsonify({'error': 'Invalid lot number'}), 400

@app.route('/api/video-stream')
def video_stream():
    lot = request.args.get('lot', '1')
    if lot not in ['1', '2']:
        return "Invalid lot number", 400
    return Response(generate_frames(lot),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# === Entry Point ===
if __name__ == '__main__':
    thread = threading.Thread(target=update_parking_data, daemon=True)
    thread.start()

    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
