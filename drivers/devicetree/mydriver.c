#include <linux/module.h>
#include <linux/init.h>
#include <linux/mod_devicetable.h>
#include <linux/property.h>
#include <linux/platform_device.h>
#include <linux/of_device.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Luyao Han");
MODULE_DESCRIPTION("An example driver using the device tree.");

static int dt_probe(struct platform_device *pdev);
static int dt_remove(struct platform_device *pdev);

static struct of_device_id my_driver_ids[] = {
    {
        .compatible = "brightlight, mydev"
    }, { }
};

MODULE_DEVICE_TABLE(of, my_driver_ids);

static struct platform_driver my_driver = {
    .probe = dt_probe,
    .remove = dt_remove,
    .driver = {
        .name = "my_device_driver",
        .of_match_table = my_driver_ids
    }
};


static int dt_probe(struct platform_device *pdev) {
    struct device *dev = &pdev->dev;
    const char *label;
    int my_value, ret;

    // Check for device properties
    if (!device_property_present(dev, "label")) {
        printk("dt_probe - Error. Device property 'label' not found");
    }

    if (!device_property_present(dev, "my_value")) {
        printk("dt_probe - Error. Device property 'my_value' not found");
    }

    // Read device properties
    ret = device_property_read_string(dev, "label", &label);
    if (ret) {
        printk("dt_probe - Error. Could not read 'label'");
    }
    printk("label: %s\n", label);

    ret = device_property_read_u32(dev, "my_value", &my_value);
    if (ret) {
        printk("dt_probe - Error. Could not read 'my_value'");
    }
    printk("my_value: %d\n", my_value);
    return 0;
}


static int dt_remove(struct platform_device *pdev) {
    printk("dt_remove - Entered dt_remove.\n");
    return 0;
}




static int __init my_init(void) {
    if (platform_driver_register(&my_driver)) {
        printk("Error. Cannot load the driver");
        return -1;
    }
    return 0;
}

static void __exit my_exit(void) {
    platform_driver_unregister(&my_driver);
}

module_init(my_init);
module_exit(my_exit);