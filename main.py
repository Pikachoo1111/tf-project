#!/usr/bin/env python3
"""
Aphasia Object Recognition System
Main application that integrates camera, object detection, button input, and audio output.
"""

import cv2
import logging
import signal
import sys
import time
from config import LOG_LEVEL, LOG_FILE, WINDOW_NAME
from button_handler import ButtonHandler
from camera_handler import CameraHandler
from object_detector import ObjectDetector
from audio_handler import AudioHandler

class AphasiaRecognitionSystem:
    """Main application class for the Aphasia Object Recognition System."""
    
    def __init__(self):
        """Initialize the system components."""
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.button_handler = None
        self.camera_handler = None
        self.object_detector = None
        self.audio_handler = None
        
        # System state
        self.running = False
        self.processing = False
        
        self.logger.info("Aphasia Object Recognition System starting...")
        
        try:
            self._initialize_components()
            self._setup_signal_handlers()
        except Exception as e:
            self.logger.error(f"Failed to initialize system: {e}")
            self.cleanup()
            raise
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def _initialize_components(self):
        """Initialize all system components."""
        self.logger.info("Initializing system components...")
        
        # Initialize camera handler
        self.camera_handler = CameraHandler()
        
        # Initialize object detector
        self.object_detector = ObjectDetector()
        
        # Initialize audio handler
        self.audio_handler = AudioHandler()
        
        # Initialize button handler and set callback
        self.button_handler = ButtonHandler()
        self.button_handler.set_callback(self.on_button_pressed)
        
        self.logger.info("All components initialized successfully")
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
    
    def on_button_pressed(self):
        """Callback function called when button is pressed."""
        if self.processing:
            self.logger.info("Already processing, ignoring button press")
            return
        
        self.logger.info("Button pressed - starting object detection")
        self.processing = True
        
        try:
            # Clear previous label
            self.camera_handler.update_display_label(None)
            
            # Capture frame for detection
            frame = self.camera_handler.capture_frame()
            if frame is None:
                self.logger.error("Failed to capture frame")
                return
            
            # Perform object detection
            label, confidence = self.object_detector.detect_objects(frame)
            
            if label:
                # Update display with detected label
                self.camera_handler.update_display_label(label, confidence)
                
                # Speak the detected object
                self.audio_handler.speak(label, blocking=False)
                
                self.logger.info(f"Detection complete: {label} ({confidence:.1%})")
            else:
                self.logger.info("No objects detected above confidence threshold")
                
        except Exception as e:
            self.logger.error(f"Error during object detection: {e}")
        finally:
            self.processing = False
    
    def run(self):
        """Main application loop."""
        try:
            self.running = True
            self.logger.info("Starting camera preview...")
            
            # Start camera preview
            self.camera_handler.start_preview()
            
            self.logger.info("System ready - press button to detect objects")
            self.logger.info("Press 'q' in the camera window or Ctrl+C to quit")
            
            # Main display loop
            while self.running:
                # Get and display current frame
                frame = self.camera_handler.get_preview_frame()
                if frame is not None:
                    self.camera_handler.show_frame(frame)
                
                # Check for quit key
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.logger.info("Quit key pressed")
                    break
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the system and cleanup resources."""
        self.logger.info("Stopping system...")
        self.running = False
        
        # Stop any ongoing speech
        if self.audio_handler:
            self.audio_handler.stop_speech()
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up all system resources."""
        self.logger.info("Cleaning up system resources...")
        
        try:
            if self.camera_handler:
                self.camera_handler.cleanup()
            
            if self.button_handler:
                self.button_handler.cleanup()
                
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
        
        self.logger.info("System shutdown complete")

def main():
    """Main entry point."""
    try:
        # Create and run the system
        system = AphasiaRecognitionSystem()
        system.run()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
