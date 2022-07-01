/**
 * @file led.c
 * @author Luyao Han (luyaohan1001@gmail.com)
 * @brief A kernel module for LED （GPIO）toggle.
 * @version 0.1
 * @date 2022-06-28
 * 
 * @copyright Copyright (c) 2022
 */

#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kdev_t.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/device.h>
#include <linux/delay.h>
#include <linux/uaccess.h>  //copy_to/from_user()
#include <linux/gpio.h>     
 
/** Macros */
#define GPIO_21 (21)
 

static struct class *dev_class;
static struct cdev led_cdev;
 
/** Function Prototypes */
static int __init led_driver_init(void);
static void __exit led_driver_exit(void);
static int led_device_open(struct inode *inode, struct file *file);
static int led_device_release(struct inode *inode, struct file *file);
static ssize_t led_device_read(struct file *filp, char __user *buf, size_t len,loff_t * off);
static ssize_t led_device_write(struct file *filp, const char *buf, size_t len, loff_t * off);
 
/** fops definition. */
static struct file_operations fops =
{
  .owner          = THIS_MODULE,
  .read           = led_device_read,
  .write          = led_device_write,
  .open           = led_device_open,
  .release        = led_device_release,
};

static int led_device_open(struct inode *inode, struct file *file)
{
    pr_info("led device has been opened.\n");
    return 0;
}

static int led_device_release(struct inode *inode, struct file *file)
{
    pr_info("led device has been closed.\n");
    return 0;
}

static ssize_t led_device_read(struct file *filp, char __user *buf, size_t len, loff_t *off)
{
    // read the gpio pin value.
    uint8_t gpio_state = gpio_get_value(GPIO_21);
  
    // write to user
    unsigned long uncopied_cnt = copy_to_user(buf, &gpio_state, 1);
    if( uncopied_cnt > 0) {
        pr_err("ERROR: Not all the bytes have been copied to user\n");
    }
  
    pr_info("Read function : GPIO_21 = %d \n", gpio_state);
    return 0;
}

static ssize_t led_device_write(struct file *filp, const char __user *buf, size_t len, loff_t *off)
{
    uint8_t p_kernel_buf[1] = {0};
    unsigned long uncopied_cnt = copy_from_user(p_kernel_buf, buf, len);

    if(uncopied_cnt > 0) {
        pr_err("ERROR: Not all the bytes have been copied from user\n");
    }

    pr_info("Write Function : GPIO_21 Set = %c\n", p_kernel_buf[0]);
    if (p_kernel_buf[0]=='1') {
        gpio_set_value(GPIO_21, 1);
    } else if (p_kernel_buf[0]=='0') {
        gpio_set_value(GPIO_21, 0);
    } else {
        pr_err("Unknown command : Please provide either 1 or 0 \n");
    }

    return len;
}

static int __init led_driver_init(void)
{
    
    // Register a range of char device numbers
    dev_t dev = 0;

    int status = alloc_chrdev_region(&dev, 0, 1, "led_device");
    if( status <=0 ) {
      pr_err("Cannot allocate major device number\n");
      goto r_unreg;
    }

    pr_info("Major = %d Minor = %d \n",MAJOR(dev), MINOR(dev));

    // Initialize char device. 
    cdev_init(&led_cdev,&fops);
 
    // Adding char device to the system.
    if((cdev_add(&led_cdev,dev,1)) < 0){
      pr_err("Cannot add the device to the system\n");
      goto r_del;
    }
 
    // Creating struct class
    if((dev_class = class_create(THIS_MODULE,"etx_class")) == NULL){
      pr_err("Cannot create the struct class\n");
      goto r_class;
    }
 
    // Create device
    if((device_create(dev_class,NULL,dev,NULL,"led_device")) == NULL){
      pr_err( "Cannot create the Device \n");
      goto r_device;
    }
  
    // Check validity of GPIO
    if(gpio_is_valid(GPIO_21) == false){
      pr_err("GPIO %d is not valid\n", GPIO_21);
      goto r_device;
    }
    // Request the GPIO
    if(gpio_request(GPIO_21,"GPIO_21") < 0){
      pr_err("ERROR: GPIO %d request\n", GPIO_21);
      goto r_gpio;
    }
    // configure the GPIO as output
    gpio_direction_output(GPIO_21, 0);
    /* Using this call the GPIO 21 will be visible in /sys/class/gpio/
     * echo 1 > /sys/class/gpio/gpio21/value  
     * echo 0 > /sys/class/gpio/gpio21/value  
     * cat /sys/class/gpio/gpio21/value  (read the value LED)
     * the second argument prevents the direction from being changed.
    */
    gpio_export(GPIO_21, false);

  
    pr_info("-> led.ko: loaded device driver to kernel.\n");
    return 0;
 
    r_gpio:
      gpio_free(GPIO_21);
    r_device:
      device_destroy(dev_class,dev);
    r_class:
      class_destroy(dev_class);
    r_del:
      cdev_del(&led_cdev);
    r_unreg:
      unregister_chrdev_region(dev,1);
  
    return -1;
}

/*
** Module exit function
*/ 
static void __exit led_driver_exit(void)
{
  gpio_unexport(GPIO_21);
  gpio_free(GPIO_21);
  device_destroy(dev_class,dev);
  class_destroy(dev_class);
  cdev_del(&led_cdev);
  unregister_chrdev_region(dev, 1);
  pr_info("-> led.ko: removed device driver from kernel.\n");
}
 

module_init(led_driver_init);
module_exit(led_driver_exit);

 
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Luyao Han <luyaohan1001@gmail.com>");
MODULE_DESCRIPTION("LCD Drvice Driver");
MODULE_VERSION("1.32");

