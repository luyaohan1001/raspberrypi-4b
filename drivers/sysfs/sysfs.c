/*****************************************************************************
 *  \file       driver.c
 *  \details    Simple Linux device driver (sysfs)
 *  \author      Luyao Han
 *  \Tested with Linux raspberrypi 5.10.103-v7l+
 *
 *******************************************************************************/
#include <linux/cdev.h>
#include <linux/device.h>
#include <linux/err.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kdev_t.h>
#include <linux/kernel.h>
#include <linux/kobject.h>
#include <linux/module.h>
#include <linux/slab.h> //kmalloc()
#include <linux/sysfs.h>
#include <linux/uaccess.h> //copy_to/from_user()

volatile int etx_value = 0;

dev_t dev = 0;
static struct class *dev_class;
static struct cdev etx_cdev;
struct kobject *kobj_ref;

/*
** Function Prototypes
*/
static int __init driver_init_callback(void);
static void __exit driver_exit_callback(void);

/*************** Driver functions **********************/
static int open_callback(struct inode *inode, struct file *file);
static int release_callback(struct inode *inode, struct file *file);
static ssize_t read_callback(struct file *filp, char __user *buf, size_t len,
                        loff_t *off);
static ssize_t write_callback(struct file *filp, const char *buf, size_t len,
                         loff_t *off);

/*************** Sysfs functions **********************/
static ssize_t sysfs_show(struct kobject *kobj, struct kobj_attribute *attr,
                          char *buf);
static ssize_t sysfs_store(struct kobject *kobj, struct kobj_attribute *attr,
                           const char *buf, size_t count);

struct kobj_attribute etx_attr =
    __ATTR(etx_value, 0660, sysfs_show, sysfs_store);

/**
 * @brief Implement function pointers.
 */
static struct file_operations fops = {
    .owner = THIS_MODULE,
    .read = read_callback,
    .write = write_callback,
    .open = open_callback,
    .release = release_callback,
};


/*
** This function will be called when we read the sysfs file
*/
static ssize_t sysfs_show(struct kobject *kobj, struct kobj_attribute *attr,
                          char *buf) {
  pr_info("Sysfs - Read\n");
  return sprintf(buf, "%d", etx_value);
}

/*
** This function will be called when we write the sysfsfs file
*/
static ssize_t sysfs_store(struct kobject *kobj, struct kobj_attribute *attr,
                           const char *buf, size_t count) {
  pr_info("Sysfs - Write\n");
  sscanf(buf, "%d", &etx_value);
  return count;
}

/*
** This function will be called when we open the Device file
*/
static int open_callback(struct inode *inode, struct file *file) {
  pr_info("Device File Opened...\n");
  return 0;
}

/*
** This function will be called when we close the Device file
*/
static int release_callback(struct inode *inode, struct file *file) {
  pr_info("Device File Closed...\n");
  return 0;
}

/*
** This function will be called when we read the Device file
*/
static ssize_t read_callback(struct file *filp, char __user *buf, size_t len,
                        loff_t *off) {
  pr_info("Read function\n");
  return 0;
}

static ssize_t write_callback(struct file *filp, const char __user *buf, size_t len,
                         loff_t *off) {
  pr_info("Write Function\n");
  return len;
}

/**
 * @brief Called when the module is inserted with insmod.
*/
static int __init driver_init_callback(void) {

  /*Allocating Major number*/
  ssize_t ret_code = alloc_chrdev_region(&dev, 0, 1, "device1001");
  if (ret_code < 0) {
    pr_info("We cannot allocate major number for our device.\n");
    return -1;
  }

  pr_info("Major = %d Minor = %d \n", MAJOR(dev), MINOR(dev));

  /*Creating cdev structure*/
  cdev_init(&etx_cdev, &fops);

  /*Adding character device to the system*/
  if ((cdev_add(&etx_cdev, dev, 1)) < 0) {
    pr_info("Cannot add the device to the system\n");
    goto r_class;
  }

  /*Creating struct class*/
  if (IS_ERR(dev_class = class_create(THIS_MODULE, "etx_class"))) {
    pr_info("Cannot create the struct class\n");
    goto r_class;
  }

  /*Creating device*/
  if (IS_ERR(device_create(dev_class, NULL, dev, NULL, "etx_device"))) {
    pr_info("Cannot create the Device 1\n");
    goto r_device;
  }

  /*Creating a directory in /sys/kernel/ */
  kobj_ref = kobject_create_and_add("etx_sysfs", kernel_kobj);

  /*Creating sysfs file for etx_value*/
  if (sysfs_create_file(kobj_ref, &etx_attr.attr)) {
    pr_err("Cannot create sysfs file......\n");
    goto r_sysfs;
  }
  pr_info("Device Driver Insert...Done\n");
  return 0;

r_sysfs:
  kobject_put(kobj_ref);
  sysfs_remove_file(kernel_kobj, &etx_attr.attr);

r_device:
  class_destroy(dev_class);
r_class:
  unregister_chrdev_region(dev, 1);
  cdev_del(&etx_cdev);
  return -1;
}

/*
** Module exit function
*/
static void __exit driver_exit_callback(void) {
  kobject_put(kobj_ref);
  sysfs_remove_file(kernel_kobj, &etx_attr.attr);
  device_destroy(dev_class, dev);
  class_destroy(dev_class);
  cdev_del(&etx_cdev);
  unregister_chrdev_region(dev, 1);
  pr_info("Device Driver Remove...Done\n");
}

/* Module init and exit points. */
module_init(driver_init_callback);
module_exit(driver_exit_callback);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Luyao Han <luyaohan1001@gmail.com>");
MODULE_DESCRIPTION("Sysfs device driver.");
MODULE_VERSION("1.0");