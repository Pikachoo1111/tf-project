#!/bin/bash

# Setup script for Aphasia Object Recognition System
# This script downloads the TensorFlow Lite model and sets up the system

set -e  # Exit on any error

echo "Setting up Aphasia Object Recognition System..."

# Create models directory
echo "Creating models directory..."
mkdir -p models

# Download TensorFlow Lite SSD MobileNet V2 model
MODEL_URL="https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip"
MODEL_ZIP="models/ssd_mobilenet_v2_coco.zip"
MODEL_FILE="models/ssd_mobilenet_v2_coco.tflite"

if [ ! -f "$MODEL_FILE" ]; then
    echo "Downloading TensorFlow Lite SSD MobileNet model..."
    wget -O "$MODEL_ZIP" "$MODEL_URL"
    
    echo "Extracting model..."
    cd models
    unzip -o ssd_mobilenet_v2_coco.zip
    
    # Rename the extracted model file to match our config
    if [ -f "detect.tflite" ]; then
        mv detect.tflite ssd_mobilenet_v2_coco.tflite
    elif [ -f "model.tflite" ]; then
        mv model.tflite ssd_mobilenet_v2_coco.tflite
    fi
    
    # Clean up
    rm -f ssd_mobilenet_v2_coco.zip
    cd ..
    
    echo "Model downloaded and extracted successfully"
else
    echo "Model already exists, skipping download"
fi

# Create COCO labels file
LABELS_FILE="models/coco_labels.txt"
if [ ! -f "$LABELS_FILE" ]; then
    echo "Creating COCO labels file..."
    cat > "$LABELS_FILE" << 'EOF'
person
bicycle
car
motorcycle
airplane
bus
train
truck
boat
traffic light
fire hydrant
stop sign
parking meter
bench
bird
cat
dog
horse
sheep
cow
elephant
bear
zebra
giraffe
backpack
umbrella
handbag
tie
suitcase
frisbee
skis
snowboard
sports ball
kite
baseball bat
baseball glove
skateboard
surfboard
tennis racket
bottle
wine glass
cup
fork
knife
spoon
bowl
banana
apple
sandwich
orange
broccoli
carrot
hot dog
pizza
donut
cake
chair
couch
potted plant
bed
dining table
toilet
tv
laptop
mouse
remote
keyboard
cell phone
microwave
oven
toaster
sink
refrigerator
book
clock
vase
scissors
teddy bear
hair drier
toothbrush
EOF
    echo "COCO labels file created"
else
    echo "Labels file already exists, skipping creation"
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y espeak espeak-data libespeak1 libespeak-dev

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Set up permissions for GPIO (if needed)
echo "Setting up GPIO permissions..."
sudo usermod -a -G gpio $USER

# Make main.py executable
chmod +x main.py

echo ""
echo "Setup complete!"
echo ""
echo "To run the system:"
echo "  python3 main.py"
echo ""
echo "Hardware setup:"
echo "  - Connect a push button between GPIO pin 21 and ground"
echo "  - Connect Raspberry Pi Camera Module to CSI port"
echo "  - Connect USB speaker for audio output"
echo "  - Connect display (HDMI or touchscreen)"
echo ""
echo "Note: You may need to log out and back in for GPIO permissions to take effect"
