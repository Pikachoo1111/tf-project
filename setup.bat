@echo off
REM Setup script for Aphasia Object Recognition System (Windows)
REM This script helps prepare the project for deployment to Raspberry Pi

echo Setting up Aphasia Object Recognition System...

REM Create models directory
echo Creating models directory...
if not exist "models" mkdir models

REM Create COCO labels file
set LABELS_FILE=models\coco_labels.txt
if not exist "%LABELS_FILE%" (
    echo Creating COCO labels file...
    (
        echo person
        echo bicycle
        echo car
        echo motorcycle
        echo airplane
        echo bus
        echo train
        echo truck
        echo boat
        echo traffic light
        echo fire hydrant
        echo stop sign
        echo parking meter
        echo bench
        echo bird
        echo cat
        echo dog
        echo horse
        echo sheep
        echo cow
        echo elephant
        echo bear
        echo zebra
        echo giraffe
        echo backpack
        echo umbrella
        echo handbag
        echo tie
        echo suitcase
        echo frisbee
        echo skis
        echo snowboard
        echo sports ball
        echo kite
        echo baseball bat
        echo baseball glove
        echo skateboard
        echo surfboard
        echo tennis racket
        echo bottle
        echo wine glass
        echo cup
        echo fork
        echo knife
        echo spoon
        echo bowl
        echo banana
        echo apple
        echo sandwich
        echo orange
        echo broccoli
        echo carrot
        echo hot dog
        echo pizza
        echo donut
        echo cake
        echo chair
        echo couch
        echo potted plant
        echo bed
        echo dining table
        echo toilet
        echo tv
        echo laptop
        echo mouse
        echo remote
        echo keyboard
        echo cell phone
        echo microwave
        echo oven
        echo toaster
        echo sink
        echo refrigerator
        echo book
        echo clock
        echo vase
        echo scissors
        echo teddy bear
        echo hair drier
        echo toothbrush
    ) > "%LABELS_FILE%"
    echo COCO labels file created
) else (
    echo Labels file already exists, skipping creation
)

echo.
echo Setup complete for Windows development!
echo.
echo To deploy to Raspberry Pi:
echo   1. Copy all files to your Raspberry Pi
echo   2. Run the setup.sh script on the Pi:
echo      chmod +x setup.sh
echo      ./setup.sh
echo   3. Run the application:
echo      python3 main.py
echo.
echo Hardware setup on Raspberry Pi:
echo   - Connect push button between GPIO pin 21 and ground
echo   - Connect Raspberry Pi Camera Module to CSI port
echo   - Connect USB speaker for audio output
echo   - Connect display (HDMI or touchscreen)

pause
