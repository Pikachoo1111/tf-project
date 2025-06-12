from gpiozero import Button
from time import sleep

# Set up Button with GPIO21 (Pin 40) and use the internal pull-up resistor
button = Button(21, pull_up=True)

# Loop to print the button state every 0.1 seconds
while True:
    if button.is_pressed:
        print("Button is pressed")
    else:
        print("Button is not pressed")
    sleep(0.1)
