#include <linux/init.h>
#include <linux/module.h>
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Luyao Han (luyaohan1001@gmail.com)");
MODULE_DESCRIPTION("Hello World module on raspberry pi 4B");

static int hello_init(void)
{
	printk(KERN_ALERT "Hello, World!\n");
	return 0;
}

static void hello_exit(void)
{
	printk(KERN_ALERT "Goodbye, World!\n");
}

module_init(hello_init);
module_exit(hello_exit);





