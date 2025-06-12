import lgpio
import time

# Open the GPIO chip
h = lgpio.gpiochip_open(0)

# Set GPIO 21 (Pin 40) as output
lgpio.gpio_claim_output(h, 2)

# Set GPIO 21 (Pin 40) to HIGH
lgpio.gpio_write(h, 2, 1)

# Keep the pin HIGH for 50 seconds
time.sleep(50)

# Cleanup
lgpio.gpiochip_close(h)
