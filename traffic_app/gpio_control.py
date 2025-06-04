# traffic_app/gpio_control.py

try:
    import RPi.GPIO as GPIO
    ON_PI = True
except ImportError:
    # For testing on non-Raspberry Pi
    ON_PI = False

import time

# Define GPIO pin numbers for red, yellow, and green lights
RED_PIN = 17
YELLOW_PIN = 27
GREEN_PIN = 22

def setup_gpio():
    if ON_PI:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RED_PIN, GPIO.OUT)
        GPIO.setup(YELLOW_PIN, GPIO.OUT)
        GPIO.setup(GREEN_PIN, GPIO.OUT)
    else:
        print("[INFO] GPIO mock setup")

def turn_on_light(color):
    if ON_PI:
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(YELLOW_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)

        if color == "red":
            GPIO.output(RED_PIN, GPIO.HIGH)
        elif color == "yellow":
            GPIO.output(YELLOW_PIN, GPIO.HIGH)
        elif color == "green":
            GPIO.output(GREEN_PIN, GPIO.HIGH)
    else:
        print(f"[MOCK] {color.upper()} light ON")

def cleanup_gpio():
    if ON_PI:
        GPIO.cleanup()
    else:
        print("[INFO] GPIO cleanup")

# Example usage
if __name__ == "__main__":
    setup_gpio()
    try:
        print("Traffic light simulation...")
        turn_on_light("red")
        time.sleep(2)
        turn_on_light("green")
        time.sleep(2)
        turn_on_light("yellow")
        time.sleep(1)
    finally:
        cleanup_gpio()
