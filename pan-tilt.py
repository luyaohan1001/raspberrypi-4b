#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import numpy as np

LASER_PINOUT = 13
FRONTLIGHT_PINOUT = 21

H_SERVO = 18
V_SERVO = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(H_SERVO, GPIO.OUT)
GPIO.setup(V_SERVO, GPIO.OUT)
GPIO.setup(FRONTLIGHT_PINOUT, GPIO.OUT)


GPIO.output(FRONTLIGHT_PINOUT, GPIO.HIGH) # Turn on

h_pwm = GPIO.PWM(H_SERVO, 50) # GPIO 17 for PWM with 50Hz
v_pwm = GPIO.PWM(V_SERVO, 50) # GPIO 17 for PWM with 50Hz


GPIO.setup(LASER_PINOUT, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
h_pwm.start(2.5) # Initialization
# v_pwm.start(10) # laser points up
# v_pwm.start(7)
v_pwm.start(5)

GPIO.output(LASER_PINOUT, GPIO.HIGH) # Turn on



        
try:
  while True:
    for i in np.arange (7.5, 9.1, 0.1):
        h_pwm.ChangeDutyCycle(i)
        time.sleep(0.05)

    for i in np.arange (9.0, 7.4, -0.1):
        h_pwm.ChangeDutyCycle(i)
        time.sleep(0.05)

    for i in np.arange (7.5, 4.9, -0.1):
        h_pwm.ChangeDutyCycle(i)
        time.sleep(0.05)


    for i in np.arange (5.0, 7.6, 0.1):
        h_pwm.ChangeDutyCycle(i)
        time.sleep(0.05)
    # GPIO.output(LASER_PINOUT, GPIO.LOW) # Turn on
    '''
    h_pwm.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    h_pwm.changedutycycle(10)
    time.sleep(0.5)
    h_pwm.ChangeDutyCycle(12.5)
    time.sleep(0.5)
    h_pwm.ChangeDutyCycle(10)
    time.sleep(0.5)
    h_pwm.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    h_pwm.ChangeDutyCycle(5)
    time.sleep(0.5)
    h_pwm.ChangeDutyCycle(2.5)
    time.sleep(0.5)
    '''
except KeyboardInterrupt:
    h_pwm.ChangeDutyCycle(5)
    h_pwm.stop()
    GPIO.cleanup()
