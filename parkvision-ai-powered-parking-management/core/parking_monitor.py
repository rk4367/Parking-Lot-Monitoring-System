import cv2
import pickle
import numpy as np
from pathlib import Path

class ParkingMonitor:
    def __init__(self):
        self.positions = []
        self.drawing = False
        self.current_idx = -1
        self.start_pos = None

        # Configuration
        self.SPOT_WIDTH, self.SPOT_HEIGHT = 90, 30
        self.OCCUPANCY_THRESHOLD = 0.2
        self.FRAME_SKIP = 1

        # Use OS-independent paths
        ASSET_DIR = Path("assets")
        self.video_paths = [
            ASSET_DIR / "video-1.mp4",
            ASSET_DIR / "video-3.mp4"
        ]
        self.pos_files = [
            ASSET_DIR / "coordinate-video-1.pkl",
            ASSET_DIR / "coordinate-video-3.pkl"
        ]
        self.original_frame_sizes = [None, None]  # To store original video dimensions

    def load_positions(self, pos_file):
        try:
            if pos_file.exists():
                with open(pos_file, 'rb') as f:
                    data = pickle.load(f)
                    if isinstance(data, list) and all(isinstance(p, (list, tuple)) and len(p) == 4 for p in data):
                        return data
                    else:
                        print(f"[ERROR] Invalid data format in {pos_file.name}: {data}")
        except Exception as e:
            print(f"Error loading positions: {e}")
        return []

    def save_positions(self, positions, pos_file):
        try:
            with open(pos_file, 'wb') as f:
                pickle.dump(positions, f)
        except Exception as e:
            print(f"Error saving positions: {e}")

    def get_config_frame(self, video_path, video_idx):
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            print(f"Error opening video: {video_path}")
            return None

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.original_frame_sizes[video_idx] = (width, height)

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return None

        frame = cv2.resize(frame, (width, height))
        return frame

    def _mouse_handler(self, event, x, y, flags, param):
        pos_file, video_idx = param

        if event == cv2.EVENT_LBUTTONDOWN:
            for i, (px, py, w, h) in enumerate(self.positions):
                if px <= x <= px + w and py <= y <= py + h:
                    self.current_idx = i
                    self.drawing = True
                    self.start_pos = (x, y)
                    return
            self.positions.append((x, y, self.SPOT_WIDTH, self.SPOT_HEIGHT))
            self.save_positions(self.positions, pos_file)

        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            if self.current_idx >= 0 and self.start_pos:
                dx, dy = x - self.start_pos[0], y - self.start_pos[1]
                px, py, w, h = self.positions[self.current_idx]
                new_w = max(20, w + dx)
                new_h = max(20, h + dy)
                self.positions[self.current_idx] = (px, py, new_w, new_h)
                self.start_pos = (x, y)
                self.save_positions(self.positions, pos_file)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.current_idx = -1

        elif event == cv2.EVENT_RBUTTONDOWN:
            for i, (px, py, w, h) in enumerate(self.positions[:]):
                if px <= x <= px + w and py <= y <= py + h:
                    self.positions.pop(i)
                    self.save_positions(self.positions, pos_file)
                    break

    def configure_spots(self, frame, pos_file, video_idx):
        original_frame = frame.copy()
        cv2.namedWindow("Configure Parking Spots", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Configure Parking Spots", self._mouse_handler, param=(pos_file, video_idx))

        print("\nConfiguration Controls:")
        print("- LEFT click: Add spot")
        print("- LEFT drag: Resize spot")
        print("- RIGHT click: Delete spot")
        print("- Press 'r' to reset")
        print("- ESC: Save and exit")

        while True:
            display_frame = original_frame.copy()
            for i, (x, y, w, h) in enumerate(self.positions):
                color = (0, 255, 255) if i == self.current_idx else (0, 255, 0)
                cv2.rectangle(display_frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(display_frame, str(i + 1), (x + 5, y + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("Configure Parking Spots", display_frame)
            key = cv2.waitKey(1)

            if key == 27:
                self.save_positions(self.positions, pos_file)
                print(f"Saved {len(self.positions)} spots")
                break
            elif key == ord('r'):
                self.positions = []
                print("Reset all spots")

        cv2.destroyWindow("Configure Parking Spots")

    def process_frame(self, frame, positions, video_idx):
        if self.original_frame_sizes[video_idx]:
            frame = cv2.resize(frame, self.original_frame_sizes[video_idx])

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 1)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 25, 16)
        processed = cv2.medianBlur(thresh, 5)
        kernel = np.ones((3, 3), np.uint8)
        processed = cv2.dilate(processed, kernel, iterations=1)

        free_count = 0
        for item in positions:
            if not isinstance(item, (tuple, list)) or len(item) != 4:
                print(f"[WARNING] Skipping invalid spot: {item}")
                continue
            x, y, w, h = item
            spot = processed[y:y + h, x:x + w]
            nonzero = cv2.countNonZero(spot)

            if nonzero > (w * h * self.OCCUPANCY_THRESHOLD):
                color = (0, 0, 255)
                thickness = 2
            else:
                color = (0, 255, 0)
                thickness = 3
                free_count += 1

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
            cv2.putText(frame, str(nonzero), (x + 5, y + h - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        status = f"Free: {free_count}/{len(positions)}"
        cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 200, 0), 2, cv2.LINE_AA)
        return frame
