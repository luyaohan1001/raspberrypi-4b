
#include <linux/module.h>
#include <linux/init.h>
#include <linux/proc_fs.h>
#include <linux/i2c.h>
#include <linux/delay.h>
#include "datalink.h"

/* Meta Information */
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Luyao Han");
MODULE_DESCRIPTION("Linux kernel module driver for ssd1306 oled display");

struct i2c_client *oled_client;

static int my_oled_probe(struct i2c_client *client, const struct i2c_device_id *id);
static int my_oled_remove(struct i2c_client *client);


static struct of_device_id my_driver_id[] = {
    {
        .compatible = "brightlight, my_oled"
    }, { /*sentinel*/ }
};

MODULE_DEVICE_TABLE(of, my_driver_id);

static struct i2c_device_id my_oled[] = {
    {
        "my_oled", 0
    }, { /*sentinel*/ }
};
MODULE_DEVICE_TABLE(i2c, my_oled);

static struct i2c_driver my_driver = {
    .probe = my_oled_probe,
    .remove = my_oled_remove,
    .id_table = my_oled,
    .driver = {
        .name = "my_oled",
        .of_match_table = my_driver_id,
    },
};



/* Entery in proc file system. This is so that this driver can be interacted with user space program. */
static struct proc_dir_entry *proc_file;

static ssize_t my_write(struct file *File, const char *user_buffer, size_t count, loff_t *offs) {
    long val;
    if ( 0 == kstrtol(user_buffer, 0, &val)) {
        i2c_smbus_write_byte(oled_client, (u8)val);
    }
    return count;
}


static ssize_t my_read(struct file *File, char *user_buffer, size_t count, loff_t *offs) {
    u8 read_val;
    read_val = i2c_smbus_read_byte(oled_client);
    return sprintf(user_buffer, "%d\n", read_val);
}

static struct proc_ops fops = {
    .proc_write = my_write,
    .proc_read = my_read,
};


static int my_oled_probe(struct i2c_client *client, const struct i2c_device_id *id) {
    printk("Entered my_oled_probe function\n");
    if (client->addr != 0x3c) {
        printk("Wrong I2C address.\n");
        return -1;
    }

    oled_client = client;
    proc_file = proc_create("my_oled", 0666, NULL, &fops);


    SSD1306_DisplayInit();
  
    //Set cursor
    // SSD1306_SetCursor(0,0);
    // SSD1306_StartScrollHorizontal( true, 0, 2);

    //Write String to OLED
    // SSD1306_String("Welcome\nTo\nEmbeTronicX\n\n");
  
    pr_info("OLED Probed!!!\n");


    return 0;
}

static int my_oled_remove(struct i2c_client *client) {
    proc_remove(proc_file);
    return 0;
}

module_i2c_driver(my_driver);