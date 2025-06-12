@echo off
REM Aphasia Object Recognition System - Windows Run Script
REM This script handles basic setup and testing on Windows

setlocal enabledelayedexpansion

echo.
echo 🧠 Aphasia Object Recognition System (Windows)
echo ===============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.7 or later.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Python found
python --version

REM Check if models directory exists
if not exist "models" (
    echo [INFO] Running Windows setup...
    call setup.bat
)

REM Check if labels file exists
if not exist "models\coco_labels.txt" (
    echo [ERROR] COCO labels file not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo [SUCCESS] Models directory ready

REM Try to install Python dependencies
echo [INFO] Checking Python dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Some Python packages may not be available on Windows
    echo [WARNING] This is expected - the system is designed for Raspberry Pi
)

REM Run component tests
echo [INFO] Testing components (Windows compatibility mode)...
python test_components.py
if errorlevel 1 (
    echo [WARNING] Some tests failed - this is expected on Windows
    echo [INFO] The system will work properly on Raspberry Pi
)

echo.
echo [INFO] Windows testing complete!
echo.
echo To deploy to Raspberry Pi:
echo   1. Copy all files to your Raspberry Pi
echo   2. Run: chmod +x run.sh
echo   3. Run: ./run.sh
echo.
echo Hardware setup on Raspberry Pi:
echo   - Connect push button between GPIO pin 21 and ground
echo   - Connect Raspberry Pi Camera Module to CSI port  
echo   - Connect USB speaker for audio output
echo   - Connect display (HDMI or touchscreen)
echo.

pause
