#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

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
	{ 0xcaec5711, "module_layout" },
	{ 0xf9a482f9, "msleep" },
	{ 0xe2888949, "i2c_del_driver" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
	{ 0x3c3ff9fd, "sprintf" },
	{ 0x82b32ac3, "proc_remove" },
	{ 0xc5850110, "printk" },
	{ 0xaa19e4aa, "_kstrtol" },
	{ 0x4e1b6800, "i2c_smbus_read_byte" },
	{ 0x2452c04d, "i2c_smbus_write_byte" },
	{ 0xcc19602c, "i2c_register_driver" },
	{ 0x86332725, "__stack_chk_fail" },
	{ 0x600d7b27, "i2c_transfer_buffer_flags" },
	{ 0x8f678b07, "__stack_chk_guard" },
	{ 0xe9a8dde7, "proc_create" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("of:N*T*Cbrightlight,_my_oled");
MODULE_ALIAS("of:N*T*Cbrightlight,_my_oledC*");
MODULE_ALIAS("i2c:my_oled");

MODULE_INFO(srcversion, "8EAA1FCBD93FB4BBA2B49F9");
