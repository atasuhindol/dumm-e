"""
camera_controller.py

Handles camera initialization, frame capture, and face detection.
Uses OpenCV Haar cascades or TensorFlow Lite for lightweight face recognition.
"""

import cv2
import numpy as np
import threading
import time
import os

class CameraController:
    def __init__(self, cascade_path=None):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("[CameraController] Unable to open camera")
        
        # Load Haar cascade for face detection
        if cascade_path is None:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        self.running = False
        self.frame = None
        self.lock = threading.Lock()
        self.thread = None

    def start_camera(self):
        """Start continuous frame capture in a separate thread."""
        if self.running:
            print("[CameraController] Camera already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._update_frames, daemon=True)
        self.thread.start()
        print("[CameraController] Camera started")
    
    def _update_frames(self):
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                print("[CameraController] Frame capture failed")
                continue
            with self.lock:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            time.sleep(0.03)  # ~30 FPS
    
    def get_frame(self):
        """Return the latest grayscale frame."""
        with self.lock:
            return self.frame.copy() if self.frame is not None else None
    
    def detect_face(self):
        """Detect face in current frame, returns True if detected."""
        frame = self.get_frame()
        if frame is None:
            return False
        faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        if len(faces) > 0:
            print(f"[CameraController] Face detected: {len(faces)} found")
            return True
        return False
    
    def stop_camera(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()
        self.camera.release()
        print("[CameraController] Camera stopped")
