obj-m := helloworld.o

KERNEL_DIR ?= /usr/src/linux-headers-$(shell uname -r)


all:
	make -C $(KERNEL_DIR) \
		ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- \
		M=$(PWD) modules

clean:
	make -C $(KERNEL_DIR) \
		ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- \
		M=$(PWD) clean

.PHONY: install-headers

install-headers:
	sudo apt install raspberrypi-kernel-headers


