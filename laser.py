#!/usr/bin/python3

# ----------------
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module

LASER_PINOUT = 13
FRONTLIGHT_PINOUT = 21

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(LASER_PINOUT, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(FRONTLIGHT_PINOUT, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
while True: # Run forever
 GPIO.output(LASER_PINOUT, GPIO.HIGH) # Turn on
 GPIO.output(FRONTLIGHT_PINOUT, GPIO.HIGH) # Turn on
 sleep(1) # Sleep for 1 second
 GPIO.output(LASER_PINOUT, GPIO.LOW) # Turn off
 GPIO.output(FRONTLIGHT_PINOUT, GPIO.LOW) # Turn off
 sleep(1) # Sleep for 1 second
