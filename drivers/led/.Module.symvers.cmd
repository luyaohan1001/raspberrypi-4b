cmd_/home/luyaohan1001/Projects/raspberrypi-4b/drivers/led/Module.symvers := sed 's/\.ko$$/\.o/' /home/luyaohan1001/Projects/raspberrypi-4b/drivers/led/modules.order | scripts/mod/modpost -m -a  -o /home/luyaohan1001/Projects/raspberrypi-4b/drivers/led/Module.symvers -e -i Module.symvers   -T -
