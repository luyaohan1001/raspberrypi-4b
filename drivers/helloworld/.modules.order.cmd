cmd_/home/pi/Projects/raspberrypi-4b/drivers/helloworld/modules.order := {   echo /home/pi/Projects/raspberrypi-4b/drivers/helloworld/helloworld.ko; :; } | awk '!x[$$0]++' - > /home/pi/Projects/raspberrypi-4b/drivers/helloworld/modules.order
