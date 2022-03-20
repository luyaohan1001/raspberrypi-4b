obj-m := helloworld-chardriver.o

KERNEL_DIR ?= /usr/src/linux-headers-5.10.103-v7l+/
CC = arm-linux-gnueabihf-gcc


all:
	make -C $(KERNEL_DIR) \
		ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- \
		M=$(PWD) modules 
	$(CC) ioctl-test.c -o ioctl-test

clean:
	make -C $(KERNEL_DIR) \
		ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- \
		M=$(PWD) clean
	rm ioctl-test


