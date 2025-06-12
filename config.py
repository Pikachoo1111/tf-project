# Configuration file for Aphasia Object Recognition System

# GPIO Configuration
BUTTON_GPIO_PIN = 21  # GPIO pin number for the physical button (configurable)
BUTTON_PULL_UP = True  # Use internal pull-up resistor

# Camera Configuration
CAMERA_RESOLUTION = (640, 480)  # Camera resolution for display
CAMERA_FRAMERATE = 30  # Camera framerate

# Object Detection Configuration
MODEL_PATH = "models/ssd_mobilenet_v2_coco.tflite"  # Path to TensorFlow Lite model
LABELS_PATH = "models/coco_labels.txt"  # Path to COCO labels file
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for object detection
MAX_DETECTIONS = 10  # Maximum number of detections to process

# Display Configuration
WINDOW_NAME = "Aphasia Object Recognition"
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
FONT_SIZE = 2
FONT_THICKNESS = 3
LABEL_COLOR = (0, 255, 0)  # Green color for label text (BGR format)
LABEL_BACKGROUND_COLOR = (0, 0, 0)  # Black background for label text

# Audio Configuration
TTS_COMMAND = "espeak"  # Text-to-speech command
TTS_PITCH = 50  # Voice pitch (1-99)
TTS_SPEED = 150  # Words per minute
TTS_VOLUME = 100  # Volume (0-200)

# Button Debouncing
DEBOUNCE_TIME = 0.3  # Minimum time between button presses (seconds)

# Logging Configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "aphasia_recognition.log"
