from evdev import InputDevice, categorize, ecodes, KeyEvent
import RPi.GPIO as GPIO
import time
import sys
import math

def main():
    joystick = InputDevice('/dev/input/event0')

    print(joystick)

    for event in joystick.read_loop():		# change duty cycle with the Nunchuk joystick
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
                duty = math.floor((absevent.event.value * 100)/255)
                print(duty)
                pwm.ChangeDutyCycle(duty) 	# Change duty cycle
                time.sleep(0.01)        	# Delay of 10mS


if __name__ == '__main__':
    try:
        led = 12			# connect red LED to the GPIO18
        GPIO.setwarnings(False)		# disable warnings
        GPIO.setmode(GPIO.BOARD)	# set pin numbering system. Using board pin numbering
        GPIO.setup(led,GPIO.OUT)
        pwm = GPIO.PWM(led,1000)	# create PWM instance with frequency
        pwm.start(0)			# started PWM at 0% duty cycle 
        main()
    except (KeyboardInterrupt, EOFError):
        ret = 0
    pwm.stop() 
    GPIO.cleanup()  
    sys.exit(ret)
