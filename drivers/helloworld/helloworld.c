
#include <linux/module.h>

static int __init hello_init(void)
{
	pr_info("-> hello world init!\n"); // pr* macros are basically printk with different severity levels.
	return 0;
}

static void __exit hello_exit(void)
{
	pr_info("-> hello world exit\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Luyao Han (luyaohan1001@gmail.com)");
MODULE_DESCRIPTION("Hello World module on raspberry pi 4B");



