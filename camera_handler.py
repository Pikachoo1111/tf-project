"""
Camera Handler for Aphasia Object Recognition System
Handles camera operations, live preview, and display overlay.
"""

import cv2
import logging
import numpy as np
from config import (
    CAMERA_RESOLUTION, CAMERA_FRAMERATE, WINDOW_NAME,
    DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT_SIZE, FONT_THICKNESS,
    LABEL_COLOR, LABEL_BACKGROUND_COLOR
)

try:
    from picamera2 import Picamera2
    PICAMERA_AVAILABLE = True
except ImportError:
    PICAMERA_AVAILABLE = False

class CameraHandler:
    """Handles camera operations and display."""
    
    def __init__(self):
        """Initialize the camera handler."""
        self.logger = logging.getLogger(__name__)
        self.camera = None
        self.is_running = False
        self.current_frame = None
        self.display_label = ""
        self.display_confidence = 0
        
        self._initialize_camera()
        self._setup_display()
    
    def _initialize_camera(self):
        """Initialize the camera (Picamera2 or USB camera)."""
        try:
            if PICAMERA_AVAILABLE:
                self.logger.info("Initializing Picamera2")
                self.camera = Picamera2()
                
                # Configure camera
                config = self.camera.create_preview_configuration(
                    main={"size": CAMERA_RESOLUTION, "format": "RGB888"}
                )
                self.camera.configure(config)
                
                self.logger.info("Picamera2 initialized successfully")
            else:
                self.logger.info("Picamera2 not available, using USB camera")
                self.camera = cv2.VideoCapture(0)
                
                if not self.camera.isOpened():
                    raise RuntimeError("Failed to open USB camera")
                
                # Set camera properties
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION[0])
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION[1])
                self.camera.set(cv2.CAP_PROP_FPS, CAMERA_FRAMERATE)
                
                self.logger.info("USB camera initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize camera: {e}")
            raise
    
    def _setup_display(self):
        """Setup the display window."""
        try:
            cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(WINDOW_NAME, DISPLAY_WIDTH, DISPLAY_HEIGHT)
            self.logger.info("Display window setup complete")
        except Exception as e:
            self.logger.error(f"Failed to setup display: {e}")
            raise
    
    def start_preview(self):
        """Start the camera preview."""
        try:
            if PICAMERA_AVAILABLE and self.camera:
                self.camera.start()
            
            self.is_running = True
            self.logger.info("Camera preview started")
            
        except Exception as e:
            self.logger.error(f"Failed to start camera preview: {e}")
            raise
    
    def stop_preview(self):
        """Stop the camera preview."""
        try:
            self.is_running = False
            
            if PICAMERA_AVAILABLE and self.camera:
                self.camera.stop()
            
            self.logger.info("Camera preview stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping camera preview: {e}")
    
    def capture_frame(self):
        """
        Capture a single frame from the camera.
        
        Returns:
            numpy.ndarray: Captured frame in BGR format, or None if failed
        """
        try:
            if PICAMERA_AVAILABLE and self.camera:
                # Capture frame from Picamera2
                frame = self.camera.capture_array()
                # Convert RGB to BGR for OpenCV
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            else:
                # Capture frame from USB camera
                ret, frame = self.camera.read()
                if not ret:
                    self.logger.error("Failed to capture frame from USB camera")
                    return None
            
            self.current_frame = frame.copy()
            self.logger.debug("Frame captured successfully")
            return frame
            
        except Exception as e:
            self.logger.error(f"Error capturing frame: {e}")
            return None
    
    def get_preview_frame(self):
        """
        Get the current preview frame with overlay.
        
        Returns:
            numpy.ndarray: Frame with overlay, or None if failed
        """
        try:
            frame = self.capture_frame()
            if frame is None:
                return None
            
            # Add overlay if there's a label to display
            if self.display_label:
                frame = self._add_label_overlay(frame, self.display_label, self.display_confidence)
            
            return frame
            
        except Exception as e:
            self.logger.error(f"Error getting preview frame: {e}")
            return None
    
    def _add_label_overlay(self, frame, label, confidence):
        """
        Add label overlay to the frame.
        
        Args:
            frame: OpenCV frame
            label: Detected object label
            confidence: Detection confidence
            
        Returns:
            numpy.ndarray: Frame with overlay
        """
        try:
            # Create label text with confidence
            label_text = f"{label} ({confidence:.1%})"
            
            # Get text size for background rectangle
            (text_width, text_height), baseline = cv2.getTextSize(
                label_text, cv2.FONT_HERSHEY_SIMPLEX, FONT_SIZE, FONT_THICKNESS
            )
            
            # Calculate position (center top of frame)
            frame_height, frame_width = frame.shape[:2]
            x = (frame_width - text_width) // 2
            y = text_height + 20  # 20 pixels from top
            
            # Draw background rectangle
            cv2.rectangle(
                frame,
                (x - 10, y - text_height - 10),
                (x + text_width + 10, y + baseline + 10),
                LABEL_BACKGROUND_COLOR,
                -1
            )
            
            # Draw text
            cv2.putText(
                frame,
                label_text,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SIZE,
                LABEL_COLOR,
                FONT_THICKNESS
            )
            
            return frame
            
        except Exception as e:
            self.logger.error(f"Error adding label overlay: {e}")
            return frame
    
    def update_display_label(self, label, confidence=0):
        """
        Update the label to display on the overlay.
        
        Args:
            label: Object label to display (None to clear)
            confidence: Detection confidence (0-1)
        """
        self.display_label = label if label else ""
        self.display_confidence = confidence
        
        if label:
            self.logger.info(f"Display label updated: {label} ({confidence:.1%})")
        else:
            self.logger.info("Display label cleared")
    
    def show_frame(self, frame):
        """
        Display a frame in the window.
        
        Args:
            frame: OpenCV frame to display
        """
        try:
            if frame is not None:
                cv2.imshow(WINDOW_NAME, frame)
        except Exception as e:
            self.logger.error(f"Error showing frame: {e}")
    
    def cleanup(self):
        """Clean up camera and display resources."""
        try:
            self.stop_preview()
            
            if PICAMERA_AVAILABLE and self.camera:
                self.camera.close()
            elif self.camera:
                self.camera.release()
            
            cv2.destroyAllWindows()
            self.logger.info("Camera handler cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
