cmd_/home/pi/Projects/raspberrypi-4b/drivers/gpio_driver/modules.order := {   echo /home/pi/Projects/raspberrypi-4b/drivers/gpio_driver/gpio_driver.ko; :; } | awk '!x[$$0]++' - > /home/pi/Projects/raspberrypi-4b/drivers/gpio_driver/modules.order