cmd_/home/pi/Projects/raspberrypi-4b/drivers/oled/modules.order := {   echo /home/pi/Projects/raspberrypi-4b/drivers/oled/oled_driver.ko; :; } | awk '!x[$$0]++' - > /home/pi/Projects/raspberrypi-4b/drivers/oled/modules.order