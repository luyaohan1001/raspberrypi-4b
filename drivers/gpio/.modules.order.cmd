cmd_/home/pi/Projects/raspi-programming/drivers/gpio/modules.order := {   echo /home/pi/Projects/raspi-programming/drivers/gpio/laser.ko; :; } | awk '!x[$$0]++' - > /home/pi/Projects/raspi-programming/drivers/gpio/modules.order
