- Class Char Drivers - 
Creating device files with devtmpfs

Before Linux 2.6.32, on basic Linux systems, the device files had to be created manually by using the mknod command. The coherency between device files and devices handled by the kernel was left to the system developer. With the release of the 2.6 series of stable kernel, a new ram-based filesystem called *sysfs* came about. 

The job of *sysfs* is to export a view of the system's hardware configuration to the user space processes. Linux drivers compiled into the kernel register their objects with a sysfs as they are detected by the kernel. For Linux drivers compiled as modules, this registration will happen when the module is loaded. Sysfs is enabled and ready to be used via the Linux kernel configuration CONFIG_SYSFS, which should be set to yes by default.

Device files are created by the kernel via the temporary *devtmpfs* filesystem. 

Any driver that wishes to register a device node will use devtmpfs (via the core driver) to do it. 

When a devtmpfs instance is mounted on /dev, the device node will initially be created with a fixed name, permissions and owner. These entries can be both read from and written to. All device nodes are owned by root and have the default mode of 0600.

Shortly afterward, the kernel will send an uevent to udevd. Based on the rules specified in the files within the 
		/etc/udev/rules.d/, 
		/lib/udev/rules.d/ and 
		/run/udev/rules.d/ directories, 

	udevd will create additional symlinks to the device node, change its permissions, owner or group, or modify the internal udevd database entry (name) for that object. The rules in these three directories are numbered, and all three directories are merged together. If udevd can't find a rule for the device it is creating, it will leave the permissions and ownership at whatever devtmpfs used initially. 

The CONFIG_DEVTMPFS_MOUNT kernel configuration option makes the kernel mounts devtmpfs automatically at boot time, except when booting on an initramfs.

LAB 4.2: "class character" module
In this kernel module lab, you will use your previous helloworld-chardriver  as a starting point, but this time, the device node will be created by using *devtmpfs* instead of doing it manually.

You will add an entry in the /sys/class/ directory. The /sys/class/ directory offers a view of the device drivers grouped by classes. 

When the register_chrdev_region() function tells the kernel that there is a driver with a specific major number, it doesn't specify anything about the type of driver, so it will not create an entry under /sys/class/. This entry is necessary so that devtmpfs can create a device node under /dev. Drivers will have a class name and a device name under the /sys folder for each created device.

A Linux driver creates/destroys the class by using the following kernel APIs:

	class_create() /* creates a class for your devices visible in /sys/class/ */
	class_destroy() /* removes the class */

A Linux driver creates the device nodes by using the following kernel APIs:

	device_create() /* creates a device node in the /dev directory */
	device_destroy() /* removes a device node in the /dev directory */

The main points that differ from your previous helloworld-chardriver driver will now be
described:

1. Include the following header file to create the class and device files:
	#include <linux/device.h> /* class_create(), device_create() */

2. Your driver will have a class name and a device name; hello_class is used as the class name and mydev as the device name. 
This results in the creation of a device that appears on the file system at /sys/class/hello_class/mydev. 
Add the following definitions for the device and class names:
	#define
	 DEVICE_NAME "mydev"
	#define
	 CLASS_NAME "hello_class"

3. The hello_init() function is longer than the one written in the helloworld-chardriver. That is because it now automatically allocates a major number to the device by using the function alloc_chrdev_region(), as well as registering the device class and creating the device node.
	static int __init hello_init(void)
	{
		dev_t dev_no;
		int Major;
		struct device* helloDevice;

		/* Allocate dynamically device numbers (only one in this driver) */
		ret = alloc_chrdev_region(&dev_no, 0, 1, DEVICE_NAME);

		/*
		* Get the device identifiers using MKDEV. We are doing this
		* for teaching purposes, as we only use one identifier in this
		* driver and dev_no could be used as a parameter for cdev_add()
		* and device_create() without needing to use the MKDEV macro
		*/

		/* Get the mayor number from the first device identifier */
		Major = MAJOR(dev_no);

		/* Get the first device identifier, that matches with dev_no */
		dev = MKDEV(Major,0);

		/* Initialize the cdev structure, and add it to kernel space */
		cdev_init(&my_dev, &my_dev_fops);
		ret = cdev_add(&my_dev, dev, 1);

		/* Register the device class */
		helloClass = class_create(THIS_MODULE, CLASS_NAME);

		/* Create a device node named DEVICE_NAME associated to dev */
		helloDevice = device_create(helloClass, NULL, dev, NULL, DEVICE_NAME);
		return 0;
}



