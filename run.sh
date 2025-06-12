#!/bin/bash

# Aphasia Object Recognition System - One-Click Run Script
# This script handles setup, dependency installation, and running the application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if running on Raspberry Pi
check_raspberry_pi() {
    if [[ ! -f /proc/device-tree/model ]] || ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
        print_warning "This doesn't appear to be a Raspberry Pi"
        print_warning "Some features may not work correctly"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "Running on Raspberry Pi"
    fi
}

# Function to check if setup has been run
check_setup_needed() {
    local setup_needed=false
    
    # Check if model exists
    if [[ ! -f "models/ssd_mobilenet_v2_coco.tflite" ]]; then
        print_status "TensorFlow Lite model not found - setup needed"
        setup_needed=true
    fi
    
    # Check if espeak is installed
    if ! command -v espeak &> /dev/null; then
        print_status "espeak not found - setup needed"
        setup_needed=true
    fi
    
    # Check if Python packages are installed
    if ! python3 -c "import cv2, numpy, gpiozero" &> /dev/null; then
        print_status "Python dependencies missing - setup needed"
        setup_needed=true
    fi
    
    if [[ "$setup_needed" == true ]]; then
        print_status "Running initial setup..."
        run_setup
    else
        print_success "System appears to be set up correctly"
    fi
}

# Function to run setup
run_setup() {
    print_status "Starting system setup..."
    
    if [[ -f "setup.sh" ]]; then
        chmod +x setup.sh
        ./setup.sh
        print_success "Setup completed"
    else
        print_error "setup.sh not found!"
        exit 1
    fi
}

# Function to test components
test_system() {
    print_status "Testing system components..."
    
    if python3 test_components.py; then
        print_success "Component tests passed"
        return 0
    else
        print_warning "Some component tests failed"
        print_warning "The system may still work, but with limited functionality"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi
}

# Function to check hardware connections
check_hardware() {
    print_status "Checking hardware setup..."
    
    # Check camera
    if command -v vcgencmd &> /dev/null; then
        camera_status=$(vcgencmd get_camera 2>/dev/null || echo "supported=0 detected=0")
        if echo "$camera_status" | grep -q "detected=1"; then
            print_success "Camera detected"
        else
            print_warning "Camera not detected"
            print_warning "Make sure the camera is connected and enabled in raspi-config"
        fi
    fi
    
    # Check GPIO access
    if [[ -r /dev/gpiomem ]] || [[ -w /dev/gpiomem ]]; then
        print_success "GPIO access available"
    else
        print_warning "GPIO access may be limited"
        print_warning "You may need to add your user to the gpio group"
    fi
    
    # Check audio devices
    if command -v aplay &> /dev/null; then
        audio_devices=$(aplay -l 2>/dev/null | grep -c "card" || echo "0")
        if [[ "$audio_devices" -gt 0 ]]; then
            print_success "Audio devices found ($audio_devices)"
        else
            print_warning "No audio devices found"
        fi
    fi
}

# Function to show hardware setup instructions
show_hardware_instructions() {
    echo
    print_status "Hardware Setup Instructions:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📱 Button Connection:"
    echo "   • GPIO Pin 21 (Physical pin 40) → Push button terminal 1"
    echo "   • Ground (any GND pin) → Push button terminal 2"
    echo "   • No resistor needed (internal pull-up used)"
    echo
    echo "📷 Camera:"
    echo "   • Connect Raspberry Pi Camera Module to CSI port"
    echo "   • Enable: sudo raspi-config → Interface Options → Camera"
    echo
    echo "🔊 Audio:"
    echo "   • Connect USB speaker to any USB port"
    echo "   • Set as default: sudo raspi-config → Advanced Options → Audio"
    echo
    echo "🖥️  Display:"
    echo "   • Connect HDMI monitor or 7\" touchscreen"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo
}

# Function to show usage instructions
show_usage_instructions() {
    echo
    print_status "Usage Instructions:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "1. 👀 The system will show a live camera preview"
    echo "2. 🔘 Press the physical button to detect objects"
    echo "3. 📝 Detected objects will appear on screen"
    echo "4. 🔊 Object names will be spoken aloud"
    echo "5. ❌ Press 'q' in the camera window to quit"
    echo "6. ⏹️  Or press Ctrl+C in this terminal to stop"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo
}

# Function to run the main application
run_application() {
    print_status "Starting Aphasia Object Recognition System..."
    
    # Make sure main.py is executable
    chmod +x main.py
    
    # Show usage instructions
    show_usage_instructions
    
    # Give user a moment to read instructions
    print_status "Starting in 3 seconds..."
    sleep 1
    print_status "Starting in 2 seconds..."
    sleep 1
    print_status "Starting in 1 second..."
    sleep 1
    
    # Run the application
    print_success "System starting now!"
    echo
    python3 main.py
}

# Function to handle cleanup on exit
cleanup() {
    print_status "Cleaning up..."
    # Kill any background processes if needed
    pkill -f "python3 main.py" 2>/dev/null || true
    print_success "Cleanup complete"
}

# Set up trap for cleanup
trap cleanup EXIT

# Main execution
main() {
    echo
    echo "🧠 Aphasia Object Recognition System"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    # Check if we're on a Raspberry Pi
    check_raspberry_pi
    
    # Check if setup is needed and run it if necessary
    check_setup_needed
    
    # Test system components
    if ! test_system; then
        print_error "System tests failed. Please check the setup."
        exit 1
    fi
    
    # Check hardware
    check_hardware
    
    # Show hardware setup instructions
    show_hardware_instructions
    
    # Ask user if they're ready
    read -p "Is your hardware connected and ready? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_status "Please connect your hardware and run this script again."
        exit 0
    fi
    
    # Run the application
    run_application
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
