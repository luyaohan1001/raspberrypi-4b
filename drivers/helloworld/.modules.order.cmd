cmd_/home/pi/Projects/raspi-programming/drivers/helloworld/modules.order := {   echo /home/pi/Projects/raspi-programming/drivers/helloworld/helloworld.ko; :; } | awk '!x[$$0]++' - > /home/pi/Projects/raspi-programming/drivers/helloworld/modules.order
