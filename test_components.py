#!/usr/bin/env python3
"""
Component Test Script for Aphasia Object Recognition System
Tests individual components to verify they work correctly.
"""

import sys
import logging
import time

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all required modules can be imported."""
    logger.info("Testing imports...")
    
    try:
        import cv2
        logger.info("✓ OpenCV imported successfully")
    except ImportError as e:
        logger.error(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        logger.info("✓ NumPy imported successfully")
    except ImportError as e:
        logger.error(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        from gpiozero import Button
        logger.info("✓ gpiozero imported successfully")
    except ImportError as e:
        logger.warning(f"⚠ gpiozero import failed (expected on non-Pi systems): {e}")
    
    try:
        from picamera2 import Picamera2
        logger.info("✓ picamera2 imported successfully")
    except ImportError as e:
        logger.warning(f"⚠ picamera2 import failed (expected on non-Pi systems): {e}")
    
    try:
        # Try TensorFlow Lite runtime first, then full TensorFlow
        try:
            import tflite_runtime.interpreter as tflite
            logger.info("✓ TensorFlow Lite runtime imported successfully")
        except ImportError:
            import tensorflow.lite as tflite
            logger.info("✓ TensorFlow Lite imported successfully")
    except ImportError as e:
        logger.error(f"✗ TensorFlow Lite import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration file."""
    logger.info("Testing configuration...")
    
    try:
        import config
        logger.info(f"✓ Config loaded - Button GPIO: {config.BUTTON_GPIO_PIN}")
        logger.info(f"✓ Model path: {config.MODEL_PATH}")
        logger.info(f"✓ Confidence threshold: {config.CONFIDENCE_THRESHOLD}")
        return True
    except Exception as e:
        logger.error(f"✗ Config test failed: {e}")
        return False

def test_audio():
    """Test audio functionality."""
    logger.info("Testing audio...")
    
    try:
        from audio_handler import AudioHandler
        audio = AudioHandler()
        logger.info("✓ Audio handler created successfully")
        
        # Test speaking (non-blocking)
        logger.info("Testing speech (you should hear 'test')...")
        success = audio.speak("test", blocking=True)
        if success:
            logger.info("✓ Speech test completed")
        else:
            logger.warning("⚠ Speech test failed (espeak may not be available)")
        
        return True
    except Exception as e:
        logger.error(f"✗ Audio test failed: {e}")
        return False

def test_camera():
    """Test camera functionality."""
    logger.info("Testing camera...")
    
    try:
        from camera_handler import CameraHandler
        
        # Try to create camera handler
        camera = CameraHandler()
        logger.info("✓ Camera handler created")
        
        # Try to capture a frame
        frame = camera.capture_frame()
        if frame is not None:
            logger.info(f"✓ Frame captured successfully - Shape: {frame.shape}")
        else:
            logger.warning("⚠ Frame capture failed (camera may not be available)")
        
        camera.cleanup()
        return True
        
    except Exception as e:
        logger.error(f"✗ Camera test failed: {e}")
        return False

def test_object_detector():
    """Test object detection functionality."""
    logger.info("Testing object detector...")
    
    try:
        from object_detector import ObjectDetector
        
        # Check if model file exists
        import os
        from config import MODEL_PATH
        
        if not os.path.exists(MODEL_PATH):
            logger.warning(f"⚠ Model file not found: {MODEL_PATH}")
            logger.info("Run setup.sh (on Pi) or setup.bat (on Windows) to download the model")
            return False
        
        # Try to create detector
        detector = ObjectDetector()
        logger.info("✓ Object detector created successfully")
        logger.info(f"✓ Model loaded with {len(detector.labels)} labels")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Object detector test failed: {e}")
        return False

def test_button():
    """Test button functionality."""
    logger.info("Testing button handler...")
    
    try:
        from button_handler import ButtonHandler
        
        # Try to create button handler
        button = ButtonHandler()
        logger.info("✓ Button handler created successfully")
        
        # Set a test callback
        def test_callback():
            logger.info("Button callback triggered!")
        
        button.set_callback(test_callback)
        logger.info("✓ Button callback set")
        
        button.cleanup()
        return True
        
    except Exception as e:
        logger.error(f"✗ Button test failed: {e}")
        return False

def main():
    """Run all component tests."""
    logger.info("Starting component tests for Aphasia Object Recognition System")
    logger.info("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Audio", test_audio),
        ("Camera", test_camera),
        ("Object Detector", test_object_detector),
        ("Button", test_button),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Testing {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{test_name:20} : {status}")
        if result:
            passed += 1
    
    logger.info(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        logger.info("🎉 All tests passed! System should work correctly.")
    else:
        logger.warning("⚠ Some tests failed. Check the errors above.")
        logger.info("Note: Some failures are expected on non-Raspberry Pi systems.")

if __name__ == "__main__":
    main()
