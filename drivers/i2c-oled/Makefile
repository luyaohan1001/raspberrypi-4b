# Target oled_driver.ko
obj-m := oled_driver.o

# The target has two objects
oled_driver-objs := driver.o datalink.o

# Run make install-headers to install kernel headers. This only works on Raspbian Buster OS.
KERNEL_DIR ?= /usr/src/linux-headers-$(shell uname -r)


# (C)hange to kernel directory, M is a variable pointing to output directory not a flag of make. 
all:
	make -C $(KERNEL_DIR) \
		ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- \
		M=$(PWD) modules

clean:
	make -C $(KERNEL_DIR) \
		ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- \
		M=$(PWD) clean
	rm -rf *.dtbo

compile_dtbo:
	dtc oled.dts -o oled.dtbo

PHONY: overlay

overlay: compile_dtbo
	sudo dtoverlay oled.dtbo
