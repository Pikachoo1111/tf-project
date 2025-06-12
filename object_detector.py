"""
Object Detector for Aphasia Object Recognition System
Handles TensorFlow Lite inference for object detection using SSD MobileNet V2.
"""

import os
import logging
import numpy as np
import cv2
from config import (
    MODEL_PATH, LABELS_PATH, CONFIDENCE_THRESHOLD, MAX_DETECTIONS
)

try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite

class ObjectDetector:
    """Handles object detection using TensorFlow Lite SSD MobileNet V2."""
    
    def __init__(self):
        """Initialize the object detector."""
        self.logger = logging.getLogger(__name__)
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.labels = []
        self.input_shape = None
        
        self._load_model()
        self._load_labels()
    
    def _load_model(self):
        """Load the TensorFlow Lite model."""
        try:
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
            
            self.logger.info(f"Loading TensorFlow Lite model: {MODEL_PATH}")
            
            # Initialize the TensorFlow Lite interpreter
            self.interpreter = tflite.Interpreter(model_path=MODEL_PATH)
            self.interpreter.allocate_tensors()
            
            # Get input and output details
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            # Get input shape
            self.input_shape = self.input_details[0]['shape']
            self.logger.info(f"Model input shape: {self.input_shape}")
            
            self.logger.info("Model loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise
    
    def _load_labels(self):
        """Load COCO labels from file."""
        try:
            if not os.path.exists(LABELS_PATH):
                self.logger.warning(f"Labels file not found: {LABELS_PATH}")
                # Create default COCO labels if file doesn't exist
                self._create_default_labels()
                return
            
            with open(LABELS_PATH, 'r') as f:
                self.labels = [line.strip() for line in f.readlines()]
            
            self.logger.info(f"Loaded {len(self.labels)} labels")
            
        except Exception as e:
            self.logger.error(f"Failed to load labels: {e}")
            self._create_default_labels()
    
    def _create_default_labels(self):
        """Create default COCO labels if labels file is not available."""
        self.labels = [
            'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
            'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
            'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
            'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
            'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
            'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
            'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
            'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
            'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
            'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
            'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
            'toothbrush'
        ]
        self.logger.info(f"Using default COCO labels ({len(self.labels)} labels)")
    
    def preprocess_image(self, image):
        """
        Preprocess image for model input.
        
        Args:
            image: OpenCV image (BGR format)
            
        Returns:
            numpy.ndarray: Preprocessed image ready for inference
        """
        # Get input dimensions from model
        input_height = self.input_shape[1]
        input_width = self.input_shape[2]
        
        # Resize image to model input size
        resized_image = cv2.resize(image, (input_width, input_height))
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values to [0, 1] if model expects float input
        if self.input_details[0]['dtype'] == np.float32:
            input_data = np.array(rgb_image, dtype=np.float32) / 255.0
        else:
            input_data = np.array(rgb_image, dtype=np.uint8)
        
        # Add batch dimension
        input_data = np.expand_dims(input_data, axis=0)
        
        return input_data
    
    def detect_objects(self, image):
        """
        Detect objects in the given image.
        
        Args:
            image: OpenCV image (BGR format)
            
        Returns:
            tuple: (best_label, confidence) or (None, 0) if no detection above threshold
        """
        try:
            if self.interpreter is None:
                self.logger.error("Model not loaded")
                return None, 0
            
            # Preprocess the image
            input_data = self.preprocess_image(image)
            
            # Set input tensor
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            
            # Run inference
            self.interpreter.invoke()
            
            # Get output tensors
            # For SSD MobileNet V2, outputs are typically:
            # - boxes: bounding box coordinates
            # - classes: class indices
            # - scores: confidence scores
            # - num_detections: number of valid detections
            
            boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
            scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]
            
            # Find the best detection above confidence threshold
            best_label = None
            best_confidence = 0
            
            for i in range(min(len(scores), MAX_DETECTIONS)):
                confidence = scores[i]
                
                if confidence > CONFIDENCE_THRESHOLD and confidence > best_confidence:
                    class_id = int(classes[i])
                    
                    # Get label name (handle potential index out of bounds)
                    if 0 <= class_id < len(self.labels):
                        label = self.labels[class_id]
                        best_label = label
                        best_confidence = confidence
                        
                        self.logger.debug(f"Detection: {label} ({confidence:.2f})")
            
            if best_label:
                self.logger.info(f"Best detection: {best_label} ({best_confidence:.2f})")
            else:
                self.logger.info("No objects detected above confidence threshold")
            
            return best_label, best_confidence
            
        except Exception as e:
            self.logger.error(f"Error during object detection: {e}")
            return None, 0
