"""
Button Handler for Aphasia Object Recognition System
Handles GPIO button input with proper debouncing logic.
"""

import time
import logging
from gpiozero import Button
from config import BUTTON_GPIO_PIN, BUTTON_PULL_UP, DEBOUNCE_TIME

class ButtonHandler:
    """Handles button input with debouncing to prevent multiple triggers."""
    
    def __init__(self):
        """Initialize the button handler."""
        self.logger = logging.getLogger(__name__)
        self.button = None
        self.last_press_time = 0
        self.callback_function = None
        
        try:
            # Initialize the button with pull-up resistor
            self.button = Button(BUTTON_GPIO_PIN, pull_up=BUTTON_PULL_UP)
            self.logger.info(f"Button initialized on GPIO pin {BUTTON_GPIO_PIN}")
        except Exception as e:
            self.logger.error(f"Failed to initialize button: {e}")
            raise
    
    def set_callback(self, callback_function):
        """
        Set the callback function to be called when button is pressed.
        
        Args:
            callback_function: Function to call when button is pressed
        """
        self.callback_function = callback_function
        if self.button:
            self.button.when_pressed = self._handle_button_press
            self.logger.info("Button callback set")
    
    def _handle_button_press(self):
        """
        Internal method to handle button press with debouncing.
        Only triggers callback if enough time has passed since last press.
        """
        current_time = time.time()
        
        # Check if enough time has passed since last press (debouncing)
        if current_time - self.last_press_time >= DEBOUNCE_TIME:
            self.last_press_time = current_time
            self.logger.debug("Button press detected (debounced)")
            
            if self.callback_function:
                try:
                    self.callback_function()
                except Exception as e:
                    self.logger.error(f"Error in button callback: {e}")
        else:
            self.logger.debug("Button press ignored (debouncing)")
    
    def is_pressed(self):
        """
        Check if button is currently pressed.
        
        Returns:
            bool: True if button is pressed, False otherwise
        """
        if self.button:
            return self.button.is_pressed
        return False
    
    def cleanup(self):
        """Clean up GPIO resources."""
        if self.button:
            self.button.close()
            self.logger.info("Button handler cleaned up")
