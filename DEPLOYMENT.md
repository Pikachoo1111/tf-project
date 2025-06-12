# Deployment Guide - Aphasia Object Recognition System

This guide explains how to deploy the system from your development environment to a Raspberry Pi.

## Quick Deployment Steps

### 1. Prepare Files for Transfer
All necessary files are ready in the current directory:
- `main.py` - Main application
- `config.py` - Configuration settings  
- `button_handler.py` - Button input handling
- `camera_handler.py` - Camera operations
- `object_detector.py` - TensorFlow Lite inference
- `audio_handler.py` - Text-to-speech
- `requirements.txt` - Python dependencies
- `setup.sh` - Raspberry Pi setup script
- `test_components.py` - Component testing
- `models/coco_labels.txt` - Object labels

### 2. Transfer to Raspberry Pi

#### Option A: Using SCP (if SSH is enabled)
```bash
# Copy entire project directory
scp -r . pi@<raspberry-pi-ip>:~/aphasia-recognition/
```

#### Option B: Using USB Drive
1. Copy all files to a USB drive
2. Insert USB drive into Raspberry Pi
3. Copy files to home directory:
   ```bash
   cp -r /media/pi/USB_DRIVE/* ~/aphasia-recognition/
   cd ~/aphasia-recognition/
   ```

#### Option C: Using Git (if repository is available)
```bash
git clone <repository-url> ~/aphasia-recognition/
cd ~/aphasia-recognition/
```

### 3. Setup and Run on Raspberry Pi

#### Option A: One-Click Setup and Run (Recommended)
```bash
cd ~/aphasia-recognition/
chmod +x run.sh
./run.sh
```

The `run.sh` script will automatically:
- Check if you're on a Raspberry Pi
- Run setup if needed (download model, install dependencies)
- Test all components
- Check hardware connections
- Show setup instructions
- Start the application

#### Option B: Manual Setup
```bash
cd ~/aphasia-recognition/
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Download TensorFlow Lite model (~10MB)
- Install system dependencies (espeak)
- Install Python packages
- Set up GPIO permissions

### 4. Hardware Connections

#### Button Wiring
- **GPIO Pin 21** (Physical pin 40) → One terminal of push button
- **Ground** (any GND pin) → Other terminal of push button
- No resistor needed (internal pull-up used)

#### Camera
- Connect Raspberry Pi Camera Module v2 to CSI port
- Enable camera: `sudo raspi-config` → Interface Options → Camera → Enable

#### Audio
- Connect USB speaker to any USB port
- Set as default: `sudo raspi-config` → Advanced Options → Audio → USB Audio

#### Display
- Connect HDMI monitor or 7" touchscreen

### 5. Test Installation
```bash
python3 test_components.py
```

This will verify all components are working correctly.

### 6. Run the Application
```bash
python3 main.py
```

## Troubleshooting Deployment

### Permission Issues
```bash
# Fix GPIO permissions
sudo usermod -a -G gpio $USER
# Log out and back in

# Make scripts executable
chmod +x setup.sh
chmod +x main.py
```

### Missing Dependencies
```bash
# Update package list
sudo apt-get update

# Install missing system packages
sudo apt-get install -y python3-pip espeak

# Install Python packages
pip3 install -r requirements.txt
```

### Camera Not Working
```bash
# Check camera detection
vcgencmd get_camera

# Enable camera interface
sudo raspi-config
# Navigate to: Interface Options → Camera → Enable
# Reboot after enabling
```

### Model Download Issues
If automatic download fails:
```bash
# Manual download
cd models/
wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
unzip coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
mv detect.tflite ssd_mobilenet_v2_coco.tflite
rm *.zip
```

### Audio Issues
```bash
# Test espeak
espeak "Hello world"

# Check audio devices
aplay -l

# Set USB audio as default
sudo raspi-config → Advanced Options → Audio → Force 3.5mm jack or Force HDMI
```

## Configuration Changes

### Change Button Pin
Edit `config.py`:
```python
BUTTON_GPIO_PIN = 18  # Change to your preferred GPIO pin
```

### Adjust Detection Sensitivity
Edit `config.py`:
```python
CONFIDENCE_THRESHOLD = 0.3  # Lower = more sensitive (0.1-0.9)
```

### Modify Display Settings
Edit `config.py`:
```python
DISPLAY_WIDTH = 1024   # Adjust for your screen
DISPLAY_HEIGHT = 768
FONT_SIZE = 3          # Larger text
```

## Performance Optimization

### For Better Performance
1. Use a fast SD card (Class 10 or better)
2. Increase GPU memory split:
   ```bash
   sudo raspi-config → Advanced Options → Memory Split → 128
   ```
3. Overclock (if cooling is adequate):
   ```bash
   sudo raspi-config → Advanced Options → Overclock
   ```

### For Lower Resource Usage
Edit `config.py`:
```python
CAMERA_RESOLUTION = (320, 240)  # Lower resolution
CAMERA_FRAMERATE = 15           # Lower framerate
```

## Auto-Start on Boot (Optional)

To start the application automatically on boot:

1. Create systemd service:
```bash
sudo nano /etc/systemd/system/aphasia-recognition.service
```

2. Add service configuration:
```ini
[Unit]
Description=Aphasia Object Recognition System
After=multi-user.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/aphasia-recognition
ExecStart=/usr/bin/python3 /home/pi/aphasia-recognition/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start service:
```bash
sudo systemctl enable aphasia-recognition.service
sudo systemctl start aphasia-recognition.service
```

## Backup and Updates

### Create Backup
```bash
tar -czf aphasia-recognition-backup.tar.gz ~/aphasia-recognition/
```

### Update System
```bash
cd ~/aphasia-recognition/
git pull  # If using git
# Or copy new files and run setup.sh again
```

## Support

If you encounter issues:
1. Check `aphasia_recognition.log` for error messages
2. Run `python3 test_components.py` to identify problems
3. Verify all hardware connections
4. Ensure all dependencies are installed
