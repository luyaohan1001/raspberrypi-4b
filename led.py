import RPi.GPIO as GPIO
import time
import os


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)


if __name__ == '__main__':
    print("LED on")
    GPIO.output(18,GPIO.HIGH)
    time.sleep(1)
    print("LED off")
    GPIO.output(18,GPIO.LOW)
