obj-m := sysfs.o

# Run make install-headers to install kernel headers. This only works on Raspbian Buster OS.
KERNEL_DIR ?= /usr/src/linux-headers-$(shell uname -r)


all:
	make -C $(KERNEL_DIR) \
		ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- \
		M=$(PWD) modules

clean:
	make -C $(KERNEL_DIR) \
		ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- \
		M=$(PWD) clean

.PHONY: install-headers run remove

run: remove
	insmod sysfs.ko

remove:
	rmmod sysfs.ko

install-headers:
	apt install raspberrypi-kernel-headers


