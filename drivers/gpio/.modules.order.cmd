cmd_/home/luyaohan1001/Projects/raspberrypi-4b/drivers/gpio/modules.order := {   echo /home/luyaohan1001/Projects/raspberrypi-4b/drivers/gpio/laser.ko; :; } | awk '!x[$$0]++' - > /home/luyaohan1001/Projects/raspberrypi-4b/drivers/gpio/modules.order
