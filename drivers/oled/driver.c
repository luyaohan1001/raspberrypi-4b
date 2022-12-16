/**
 * @file driver.c
 * @brief Kernel layers i2c device driver implementation.
*/
#include <linux/module.h>
#include <linux/i2c.h>
#include <linux/delay.h>
#include "datalink.h"


/* Loadable kernel module license registration. */
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Luyao Han");
MODULE_DESCRIPTION("Linux kernel module driver for ssd1306 oled display");

/* Function Signatures. */
static int driver_on_probe(struct i2c_client *client, const struct i2c_device_id *id);
static int driver_on_remove(struct i2c_client *client);

/* File static variables. */
struct i2c_client *i2c_client;

/**
 * @brief Specifies the ".compatible" strings.
 *          of_device_id array should store the same value as corresponding node's "compatible" field in the device tree.
 *          In this case the oled.dts in the same directory has the "compatible" field.
 *          When the .compatible field here matches the device tree, the I2C device will be probed.
*/
static struct of_device_id driver_id[] = {
    {
        .compatible = "ssd1306, oled_device"
    }, { /*sentinel*/ }
};
MODULE_DEVICE_TABLE(of, driver_id);

/**
 * @brief This array is pointed by the id_table field of struct i2c_driver.
 *          The id_table is used for non-DT based probing of I2C-devices.
*/

static struct i2c_device_id driver_device_id[] = {
    {
        "oled_device", 0
    }, { /*sentinel*/ }
};

MODULE_DEVICE_TABLE(i2c, driver_device_id);

/* Instantiate i2c driver. */
static struct i2c_driver i2c_driver = {
    /* Callbacks for the driver entry / exit. */
    .probe = driver_on_probe,
    .remove = driver_on_remove,
    .id_table = driver_device_id,
    .driver = {
        .name = "oled_device",
        .of_match_table = driver_id,
    },
};

/**
 * @brief Callback function on probing (driver-device binding) of the device driver.
 * @param client Pointer to the i2c_client instance. 
 * @param device_id The device id to be probed.
 * @return Error status. 
*/
static int driver_on_probe(struct i2c_client *client, const struct i2c_device_id *device_id) {
    int statusCode = 0;
    pr_info("Entered driver_on_probe function\n");

    if (client->addr != 0x3c) {
        pr_info("Wrong I2C address.\n");
        statusCode = -1;
        goto RETURN;
    } else {
        pr_info("OLED with I2C address 0x3C has been successfully probed.\n");
    }

    /* Binding instance to the probed i2c client. */
    i2c_client = client;

    /* Entry to the OLED display logic. */
    ssd1306_display_init();
    
    RETURN:
        return statusCode;
}

/**
 * @brief Callback function on the removal of the device driver.
 * @param client Pointer to the i2c_client instance.
 * @return Status code.
*/
static int driver_on_remove(struct i2c_client *client) {
    int statusCode = 0;
    return statusCode;
}

module_i2c_driver(i2c_driver);