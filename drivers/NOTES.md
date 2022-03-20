If we compile Loadable Kernel Modules, the kernel source needs to be specified by the KERNEL_DIR variable.
If we are simply compiling the LKM on raspberrypi, and loading the module on raspberry-pi, the kernel source can be obtained by:

	$ sudo apt update

	$ sudo apt install raspberrypi-kernel-headers

The kernel location will be at, for example:
	
	$ cd /usr/src/linux-headers-5.10.103-v7l+/

In the Makefile, simply set 
	KERNEL_DIR ?= /usr/src/<linux-headers-directory>/

Now we can run 

	$ make 

	in the LKM development folder.

Insert the module by:

	$ sudo insmod <module-name>.ko

The module will be loaded at locaion found by:

	$ find /sys/ -name '*helloworld*'
	-> /sys/module/helloworld


---- ---- ---- ---- ---- ---- ---- ----

If, alternatively, we are compiling on a X86 machine and running the module on raspberry-pi, the kernel source repository needs to be downloaded:
 	$ git clone https://github.com/raspberrypi/linux.git	

The release we select on this git repository needs to be the same with the one running on the raspberry pi:
	$ uname -a

	-> Linux raspberrypi 5.10.92-v7l+ #1514 SMP Mon Jan 17 17:38:03 GMT 2022 armv7l GNU/Linux

	$ git checkout raspi-5.10.y...

	We have selected the 5.10.y release.

Once this directory is cloned, enter the ./linux directory, proper config is needed:

	$ cd /arch/arm/configs

	This directory have the config file for many different platforms. The chipset we use for Raspberry-Pi model 4B is BCM2711. Thus,


	$ sudo apt install git bc bison flex libssl-dev make libc6-dev libncurses5-dev

	$ make bcm2711_defconfig

	-> 

		  LEX     scripts/kconfig/lexer.lex.c
		  YACC    scripts/kconfig/parser.tab.[ch]
		  HOSTCC  scripts/kconfig/lexer.lex.o
		  HOSTCC  scripts/kconfig/menu.o
		  HOSTCC  scripts/kconfig/parser.tab.o
		  HOSTCC  scripts/kconfig/preprocess.o
		  HOSTCC  scripts/kconfig/symbol.o
		  HOSTCC  scripts/kconfig/util.o
		  HOSTLD  scripts/kconfig/conf
		#
		# configuration written to .config
		#

		

	
