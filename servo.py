#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import math





class Truck():
    def __init__(self):
        self.pwm = None
        self.curr_pwm = 0.0
        self.STEER_MIDDLE = 8.0
        self.LEFT_MAX = 6.0
        self.RIGHT_MAX = 9.25

    def gpio_init(self, curr_pwm=0.0):
        servoPIN = 13
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)

        self.pwm = GPIO.PWM(servoPIN, 50) # PWM Period
        self.pwm.start(self.STEER_MIDDLE) # Initialization
        self.curr_pwm = self.STEER_MIDDLE


    def pwm_damped_steering(self, target_pwm):
        '''
            Steer to a specific pwm gradually to make the steering look natural.
        '''
        granularity = 0.1
        pwm_diff = target_pwm - self.curr_pwm
        print(pwm_diff)

        while not abs(self.curr_pwm - target_pwm) < 0.101:

            if (self.curr_pwm < target_pwm):
                self.curr_pwm += granularity
            else:
                self.curr_pwm -= granularity

            # Limit number of decimals to remove servo jitter.
            self.curr_pwm = round(self.curr_pwm, 4)
            print('.' + str(self.curr_pwm))
            # print(self.curr_pwm)
            self.pwm.ChangeDutyCycle(self.curr_pwm)
            time.sleep(0.005)


    def front_wheels_steer(self):
        try:
          while True:

            # Get user input
            duty_cycle = float(input('Enter duty cycle (float between '+ str(self.LEFT_MAX) + ' to ' + str(self.RIGHT_MAX) + '):\n> '))
            
            if duty_cycle > self.RIGHT_MAX:
                duty_cycle = self.RIGHT_MAX
            elif duty_cycle < self.LEFT_MAX:
                duty_cycle = self.LEFT_MAX
            elif not isinstance(duty_cycle, float):
                duty_cycle = self.STEER_MIDDLE


            self.pwm.ChangeDutyCycle(duty_cycle)
            # self.pwm_damped_steering(duty_cycle)
            self.curr_pwm = duty_cycle
            print('Duty cycle was set to {} %'.format(duty_cycle))
            #time.sleep(0.5)

        except KeyboardInterrupt:
          self.pwm.stop()
          GPIO.cleanup()

if __name__ == '__main__':
    chevy = Truck()
    chevy.gpio_init()
    chevy.front_wheels_steer()
