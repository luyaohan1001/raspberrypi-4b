#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x38f431f2, "module_layout" },
	{ 0xb6a5752c, "gpiod_unexport" },
	{ 0x6091b333, "unregister_chrdev_region" },
	{ 0x48a84465, "cdev_del" },
	{ 0xec6c724b, "class_destroy" },
	{ 0x4bcfdc97, "device_destroy" },
	{ 0x57c53bd2, "gpiod_export" },
	{ 0x2030d859, "gpiod_direction_output_raw" },
	{ 0xfe990052, "gpio_free" },
	{ 0x47229b5c, "gpio_request" },
	{ 0x761d47c4, "device_create" },
	{ 0x11ddfbc6, "__class_create" },
	{ 0xe023ffe0, "cdev_add" },
	{ 0x285cb869, "cdev_init" },
	{ 0xe3ec2f2b, "alloc_chrdev_region" },
	{ 0x2e1e487f, "gpiod_set_raw_value" },
	{ 0x2cfde9a2, "warn_slowpath_fmt" },
	{ 0x5f754e5a, "memset" },
	{ 0xae353d77, "arm_copy_from_user" },
	{ 0x8f678b07, "__stack_chk_guard" },
	{ 0x3ea1b6e4, "__stack_chk_fail" },
	{ 0x51a910c0, "arm_copy_to_user" },
	{ 0x3376ec94, "gpiod_get_raw_value" },
	{ 0xeaf06972, "gpio_to_desc" },
	{ 0x92997ed8, "_printk" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "C4A9EE1D37A65B52DF44592");
