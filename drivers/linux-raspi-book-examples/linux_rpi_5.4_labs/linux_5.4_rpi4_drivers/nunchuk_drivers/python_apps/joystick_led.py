from evdev import InputDevice, categorize, ecodes, KeyEvent
from gpiozero import LED
import sys

def main():
    joystick = InputDevice('/dev/input/event0')

    print(joystick)

    for event in joystick.read_loop():

        if event.type == ecodes.EV_KEY:
            keyevent = categorize(event)
            if keyevent.keycode == 'BTN_C':
                if keyevent.keystate == KeyEvent.key_down:
                    led.on()
                elif keyevent.keystate == KeyEvent.key_up:
                    led.off()

        elif event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
                if absevent.event.value > 126: 
                    print('right')   
                    print(absevent.event.value)
                elif absevent.event.value < 126: 
                    print('left') 
                    print(absevent.event.value)
                elif absevent.event.value == 126: 
                    print('centered') 
                    print(absevent.event.value)


if __name__ == '__main__':
    try:
        led = LED(17) 
        main()
    except (KeyboardInterrupt, EOFError):
        ret = 0
    led.close()
    sys.exit(ret)

		
