Character Drivers - Chapter 4
Typically, an operating system is designed to hide the underlying hardware details from the user application. Applications do, however, require the ability to access data that is captured by hardware peripherals, as well as the ability to drive peripherals with output. 

Since the peripheral registers are accessible only by the Linux kernel, only the kernel is able to collect data streams as they are captured by these peripherals.
Linux requires a mechanism to transfer data from kernel to user space. This transfer of data is handled via *device nodes*, which are also known as *virtual files*. 

Device nodes exist within the root filesystem, though they are not true files. 

When a user reads from a device node, the kernel copies the data stream captured by the underlying driver into the application memory space.

When a user writes to a device node, the kernel copies the data stream provided by the application into the data buffers of the driver, which are eventually output via the underlying hardware. 

These virtual files can be "opened" and "read from" or "written to" by the user application using standard system calls.

Each device has a unique driver that handles requests from user applications that are eventually passed to the core. 

Linux supports three types of devices: 
	character devices
	block devices
	network devices. 

While the concept is the same, the difference in the drivers for each of these devices is the manner in which the files are "opened" and "read from" or "written to". 

Character devices are the most common devices, which are read and written directly without buffering, for example:

	keyboards
	monitors
	printers
	serial ports

Block devices can only be written to and read from in multiples of the block size, typically 512 or 1024 bytes. They may be randomly accessed, i.e., any block can be read or written no matter where it is on the device. A classic example of a block device is a hard disk drive. Network devices are accessed via the BSD socket
interface and the networking subsystems.

Character devices are identified by a *c* in the first column of a listing, and block devices are identified by a *b*. The access permissions, owner and group of the device are provided for each device.


From the point of view of an application, a character device is essentially a file. A process only knows a /dev file path. The process opens the file by using the open() system call and performs standard file operations like read() and write().

In order to achieve this, a character driver must implement the operations described in the *file_operations* structure (declared in include/linux/fs.h in the kernel source tree) and register them. 

In the file_operations structure shown below, you can see some of the most common operations for a character driver:

  struct file_operations {
    struct module *owner;
    loff_t (*llseek) (struct file *, loff_t, int);
    ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
    ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);
    long (*unlocked_ioctl) (struct file *, unsigned int, unsigned long);
    int (*mmap) (struct file *, struct vm_area_struct *);
    int (*open) (struct inode *, struct file *);
    int (*release) (struct inode *, struct file *);
  };

The Linux filesystem layer will ensure that these operations are called when a user space application makes the corresponding system call (on the kernel side, the driver implements and registers the callback operation).


- How does the kernel exchange data with user space? -

The kernel driver will use the specific functions *copy_from_user()* and *copy_to_user()* to exchange data with user space, as shown in the previous figure.

Both the read() and write() methods return a negative value if an error occurs. A return value greater than or equal to 0, instead, tells the calling program how many bytes have been successfully transferred. 

If some data is transferred correctly and then an error happens, the return value must be the count of bytes successfully transferred, and the error does not get reported until the next time the function is called. 

Implementing this convention requires, of course, that your driver remember that the error has occurred so that it can return the error status in the future.

The return value for read() is interpreted by the calling application program:
	1. If the value equals the count argument passed to the read system call, the requested number of bytes has been transferred. This is the optimal case.

	2. If the value is positive, but smaller than the count, then only part of the data has been transferred. This may happen for a number of reasons, depending on the device. Most often, the application program retries the read. For instance, if you read using the fread() function, the library function reissues the system call until completion of the requested data transfer. If the value is 0, end-of-file was reached.

	3. A negative value means there was an error. The value specifies what the error was, according to <linux/errno.h>. Typical values returned on error include -EINTR (interrupted system call) or -EFAULT (bad address).

- Major and Minor device number -
	In Linux, every device is identified by two numbers: a major number and a minor number. These numbers can be seen by invoking ls -l /dev on the host PC. Every device driver registers its major number with the kernel and is completely responsible for managing its minor numbers. 

When accessing a device file, the major number selects which device driver is being called to perform the input/output operation. The major number is used by the kernel to identify the correct device driver when the device is accessed. 

The role of the minor number is device dependent and is handled internally within the driver. For instance, the Raspberry Pi has several hardware UART
ports. The same driver can be used to control all the UARTs, but each physical UART needs its own device node, so the device nodes for these UARTs will all have the same major number, but will have unique minor numbers.


- LAB 4.1: "helloworld character" module -
Linux systems in general traditionally used a static device creation method, whereby a great number of device nodes were created under /dev (sometimes literally thousands of nodes), regardless of whether or not the corresponding hardware devices actually existed. This was typically done via a MAKEDEV script, which contains a number of calls to the mknod program with the relevant major and minor device numbers for every possible device that might exist in the world.

This is not the right approach to create device nodes nowadays, as you have to create a block or character device file entry manually and associate it with the device, as shown in the Raspberry Pi ́s terminal command line below:

  $ mknod /dev/mydev c 202 108

We will develop this driver using the static method, purely for education purposes.

Despite all this, you will develop your next driver using this static method, purely for educational purposes, and you will see in the few next drivers a better way to create the device nodes by using devtmpfs and the miscellaneous framework.

In this kernel module lab, you will interact with user space through an ioctl_test user application. You will use open() and ioctl() system calls in your application, and you will write its corresponding driver ́s callback operations on the kernel side, providing a communication between user and kernel space.

In the first lab, you saw what a basic driver looks like. This driver didn’t do much except printing some text during installation and removal. In the following lab, you will expand this driver to create a device with a major and minor number. You will also create a user application to interact with the driver.

Finally, you will handle file operations in the driver to service requests from user space.

In the kernel, a character-type device is represented by struct cdev, a structure used to register it in the
system.



- Registration and unregistration of character devices -

The registration/unregistration of a character device is made by specifying the major and minor.


The *dev_t* type is used to keep the identifiers of a device (both major and minor) and can be obtained by using the MKDEV macro.

For the static assignment and unallocation of device identifiers, the *register_chrdev_region()* and *unregister_chrdev_region()* functions are used. The first device identifier is obtained by using the MKDEV macro.

  int register_chrdev_region(dev_t first, unsigned int count, char *name);

  void unregister_chrdev_region(dev_t first, unsigned int count);

It is recommended that device identifiers be dynamically assigned by using the *alloc_chrdev_region()* function. This function allocates a range of char device numbers. The major number will be chosen dynamically and returned (along with the first minor number) in dev. This function returns
zero or a negative error code.

  int alloc_chrdev_region(dev_t* dev, unsigned baseminor, unsigned count, const char* name);

See below the description of the arguments of the previous function:

  dev: Output parameter for first assigned number.
  baseminor: First of the requested range of minor numbers.
  count: Number of minor numbers required.
  name: Name of the associated device or driver.

In the line of code below, the second parameter reserves a number (my_minor_count) of devices, starting with my_major major and my_first_minor minor. The first parameter of the register_chrdev_region() function is the first identifier of the device. The successive identifiers can be retrieved by
using the MKDEV macro.

  register_chrdev_region(MKDEV(my_major, my_first_minor), my_minor_count, "my_device_driver");

After assigning the identifiers, the character device will have to be initialized by using the cdev_ init() function and registered to the kernel by using the cdev_add() function. The cdev_init() and cdev_add() functions will be called as many times as assigned device identifiers.

The following sequence registers and initializes a number (MY_MAX_MINORS) of devices:

#include <linux/fs.h>
#include <linux/cdev.h>
#define MY_MAJOR 42
#define MY_MAX_MINORS 5

struct my_device_data {

struct cdev cdev;
  /* my data starts here */
  [...]
};
struct my_device_data devs[MY_MAX_MINORS];

const struct file_operations my_fops = {
  .owner = THIS_MODULE,
  .open = my_open,
  .read = my_read,
  .write = my_write,
  .release = my_release,
  .unlocked_ioctl = my_ioctl
};

int init_module(void)
{
  int i, err;
  register_chrdev_region(MKDEV(MY_MAJOR, 0), MY_MAX_MINORS, "my_device_driver");
  for(i = 0; i < MY_MAX_MINORS; i++) {
  /* initialize devs[i] fields and register character devices */
  cdev_init(&devs[i].cdev, &my_fops);
  cdev_add(&devs[i].cdev, MKDEV(MY_MAJOR, i), 1);
}
  return 0;
}

The following code snippet deletes and unregisters the character devices:
void cleanup_module(void)
{
	int i;
}
for(i = 0; i < MY_MAX_MINORS; i++) {
/* release devs[i] fields */
	cdev_del(&devs[i].cdev);
}

unregister_chrdev_region(MKDEV(MY_MAJOR, 0), MY_MAX_MINORS);

The main code sections of the driver will now be described:
1. Include the folowing header files to support character devices:
	#include <linux/cdev.h>
	#include <linux/fs.h>

2. Define the major number:
	#define MY_MAJOR_NUM 202

3. One of the first things your driver will need to do when setting up a char device is to obtain one or more device identifiers (major and minor numbers) to work with. The necessary function for this task is register_chrdev_region(), which is declared in include/linux/ fs.h in the kernel source tree. Add the following lines of code to the hello_init() function to allocate the device numbers when the module is loaded. The MKDEV macro will combine a major number and a minor number to a dev_t data type that is used to hold the first device identifier.

	dev_t dev = MKDEV(MY_MAJOR_NUM, 0); /* get first device identifier */
	/*
	* Allocates all the character device identifiers,
	* only one in this case, the one obtained with the MKDEV macro
	*/
	register_chrdev_region(dev, 1, "my_char_device");

4. Add the following line of code to the hello_exit() function to return the devices when the module is removed:
	unregister_chrdev_region(MKDEV(MY_MAJOR_NUM, 0), 1);

5. Create a file_operations structure called my_dev_fops. This structure defines function pointers for "opening", "reading from", "writing to" the device, etc.

  static const struct file_operations my_dev_fops = {
  .owner = THIS_MODULE,
  .open = my_dev_open,
  .release = my_dev_close,
  .unlocked_ioctl = my_dev_ioctl,
  };

6. Implement each of the callback functions that are declared in the file_operations structure:
  static int my_dev_open(struct inode *inode, struct file *file)
  {
  pr_info("my_dev_open() is called.\n");
  return 0;
  }
  static int my_dev_close(struct inode *inode, struct file *file)
  {
  pr_info("my_dev_close() is called.\n");
  return 0;
  }
  static long my_dev_ioctl(struct file *file, unsigned int cmd, 				
  unsigned long arg)
  {
  pr_info("my_dev_ioctl() is called. cmd = %d, arg = %ld\n", cmd, arg);
  return 0;
  }

7. Add these file operation functionalities to your character device. The Linux kernel uses struct cdev to represent character devices internally; therefore you will create a struct cdev variable called my_dev and initialize it by using the cdev_init() function call, which takes the variable my_dev and the structure my_dev_fops as parameters. Once the cdev structure is setup, you will tell the kernel about it by using the cdev_add() function. You will call cdev_init() and cdev_add() as many times as allocated character device identifiers (only once in this driver).

  static struct cdev my_dev;
  cdev_init(&my_dev, &my_dev_fops);
  ret= cdev_add(&my_dev, dev, 1);

8.Add the following line of code to the hello_exit() function to delete the cdev structure:
  cdev_del(&my_dev);

9. Once the kernel module has been dynamically loaded, the user needs to create a device node to reference the driver. Linux provides the mknod utility for this purpose. The mknod command has four parameters. The first parameter is the name of the device node that will be created. The second parameter indicates whether the driver to which the device node interfaces is a block driver or character driver. The last two parameters passed to mknod are the major and minor numbers. Assigned major numbers are listed in the /proc/devices file and can be viewed using the cat command. The created device node should be placed in the /dev directory.

10. Create a new helloword_rpi3_char_driver.c file in the linux_5.4_rpi3_drivers folder, and write the Listing 4-1 code on it. Add helloword_rpi3_char_driver.o to your Makefile obj-m variable.

11. In the linux_5.4_rpi3_drivers folder, you will create the apps folder, where you are going to store most of the applications developed through this book. ~/linux_5.4_rpi3_drivers$ mkdir apps

12.In the apps folder, you will create an ioctl_test.c file, then write the Listing 4-3 code on it. You will also create a Makefile (Listing 4-2) file in the apps folder to compile and deploy the application.

$ Make

# To insert the kernel module.
$ insmod helloworld-chardriver.ko

$ dmesg

	-> hello world char driver init!

See the allocated "my_char_device". The device mydev is not created under /dev yet:

$ cat /proc/devices

Character devices:
1 mem
4 /dev/vc/0
4 tty
4 ttyS
5 /dev/tty
5 /dev/console
[...]
202 my_char_device
[...]

$ /home/pi# ls –l /dev/
Create mydev under /dev using mknod, and verify its creation:

$ mknod /dev/mydev c 202 0
$ ls -l /dev/mydev
-> crw-r--r-- 1 root root 202, 0 Apr 8 19:00 /dev/mydev

Run the application ioctl_test:
$ ./ioctl_test
$ dmesg
my_dev_open() is called.
my_dev_ioctl() is called. cmd = 100, arg = 110
my_dev_close() is called.

# Remove the module:
$ rmmod helloworld-chardriver.ko
$ dmesg
-> hello world char driver exit!


