cmd_/home/pi/Projects/raspberrypi-4b/drivers/sysfs/modules.order := {   echo /home/pi/Projects/raspberrypi-4b/drivers/sysfs/sysfs.ko; :; } | awk '!x[$$0]++' - > /home/pi/Projects/raspberrypi-4b/drivers/sysfs/modules.order
