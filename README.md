# Aphasia Object Recognition System

A Raspberry Pi application designed to help individuals with aphasia by providing object recognition through a simple button-triggered interface. The system displays a live camera feed, detects objects when a button is pressed, and provides both visual and audio feedback.

## Features

- **Button-activated detection**: Object recognition runs only when the user presses a physical button
- **Live camera preview**: Continuous display of camera feed
- **Visual feedback**: Shows detected object labels on screen with confidence scores
- **Audio feedback**: Speaks object names aloud through USB speaker
- **Debounce logic**: Prevents repeated detections from button bouncing
- **Configurable GPIO**: Easy to change button pin assignment
- **High accuracy**: Uses TensorFlow Lite SSD MobileNet V2 with COCO dataset

## Hardware Requirements

- Raspberry Pi 4 or 5
- Raspberry Pi Camera Module v2 (CSI connection)
- Display (7" touchscreen or HDMI monitor)
- USB external speaker for audio output
- Physical push-button
- Jumper wires and breadboard (for button connection)

## Hardware Setup

### Button Connection
1. Connect one terminal of the push button to **GPIO pin 21** (Physical pin 40)
2. Connect the other terminal to **Ground** (any GND pin)
3. The internal pull-up resistor is used, so no external resistor is needed

### Camera Connection
1. Connect the Raspberry Pi Camera Module to the CSI port
2. Enable the camera interface: `sudo raspi-config` → Interface Options → Camera → Enable

### Audio Setup
1. Connect USB speaker to any USB port
2. Set USB speaker as default audio output:
   ```bash
   sudo raspi-config
   # Navigate to: Advanced Options → Audio → USB Audio
   ```

## Software Installation

### 1. Clone or Download
```bash
# If using git:
git clone <repository-url>
cd aphasia-object-recognition

# Or download and extract the files to a directory
```

### 2. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Download the TensorFlow Lite SSD MobileNet V2 model
- Create COCO labels file
- Install system dependencies (espeak)
- Install Python dependencies
- Set up GPIO permissions

### 3. Manual Installation (Alternative)
If the setup script doesn't work, install manually:

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y espeak espeak-data python3-pip

# Install Python dependencies
pip3 install -r requirements.txt

# Create models directory and download model
mkdir -p models
# Download model manually from TensorFlow Model Zoo
```

## Configuration

Edit `config.py` to customize settings:

```python
# Change button GPIO pin
BUTTON_GPIO_PIN = 21  # Change to your preferred GPIO pin

# Adjust detection sensitivity
CONFIDENCE_THRESHOLD = 0.5  # Lower = more sensitive, Higher = more selective

# Modify display settings
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# Audio settings
TTS_PITCH = 50  # Voice pitch (1-99)
TTS_SPEED = 150  # Words per minute
```

## Usage

### Quick Start (Recommended)
```bash
# Make the run script executable
chmod +x run.sh

# Run everything automatically
./run.sh
```

The `run.sh` script will:
- Check if you're on a Raspberry Pi
- Run setup automatically if needed
- Test all components
- Check hardware connections
- Show setup instructions
- Start the application

### Manual Start
```bash
python3 main.py
```

### Operation
1. The system starts and displays a live camera feed
2. Point the camera at objects you want to identify
3. Press the physical button to trigger object detection
4. The system will:
   - Capture the current camera frame
   - Analyze it for objects
   - Display the detected object name on screen
   - Speak the object name through the speaker
5. Press 'q' in the camera window or Ctrl+C to quit

### System Behavior
- **Button press**: Triggers one detection cycle
- **No detection**: If no object is detected above the confidence threshold, nothing is displayed or spoken
- **Debouncing**: Multiple rapid button presses are ignored to prevent repeated detections
- **Processing indicator**: The system ignores button presses while processing a detection

## File Structure

```
aphasia-object-recognition/
├── main.py                 # Main application
├── config.py              # Configuration settings
├── button_handler.py      # Button input handling
├── camera_handler.py      # Camera operations and display
├── object_detector.py     # TensorFlow Lite inference
├── audio_handler.py       # Text-to-speech functionality
├── requirements.txt       # Python dependencies
├── setup.sh              # Raspberry Pi setup script
├── setup.bat             # Windows setup script
├── run.sh                # One-click run script (Raspberry Pi)
├── run.bat               # Windows run script
├── test_components.py    # Component testing
├── README.md             # This file
├── DEPLOYMENT.md         # Deployment guide
└── models/               # Model files (created by setup)
    ├── ssd_mobilenet_v2_coco.tflite
    └── coco_labels.txt
```

## Troubleshooting

### Camera Issues
```bash
# Check if camera is detected
vcgencmd get_camera

# Enable camera interface
sudo raspi-config
```

### GPIO Permission Issues
```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER
# Log out and back in
```

### Audio Issues
```bash
# Test espeak
espeak "Hello world"

# Check audio devices
aplay -l

# Set USB audio as default
sudo raspi-config → Advanced Options → Audio
```

### Model Download Issues
If the automatic model download fails:
1. Manually download from [TensorFlow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md)
2. Extract to `models/` directory
3. Rename to `ssd_mobilenet_v2_coco.tflite`

## Customization

### Changing Button Pin
Edit `config.py`:
```python
BUTTON_GPIO_PIN = 18  # Change to your preferred pin
```

### Adding Custom Labels
Edit `models/coco_labels.txt` to modify object names for better pronunciation or localization.

### Adjusting Sensitivity
Lower `CONFIDENCE_THRESHOLD` in `config.py` for more detections, raise it for fewer false positives.

## Performance Notes

- First detection may be slower due to model loading
- Subsequent detections are typically faster
- Performance varies by Raspberry Pi model and SD card speed
- Consider using a high-speed SD card (Class 10 or better)

## License

This project is open source. Please check individual component licenses for TensorFlow Lite and other dependencies.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review log files (`aphasia_recognition.log`)
3. Ensure all hardware connections are correct
4. Verify all dependencies are installed
