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
	{ 0xe2888949, "i2c_del_driver" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
	{ 0xc5850110, "printk" },
	{ 0xcc19602c, "i2c_register_driver" },
	{ 0x86332725, "__stack_chk_fail" },
	{ 0x600d7b27, "i2c_transfer_buffer_flags" },
	{ 0x8f678b07, "__stack_chk_guard" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("of:N*T*Cssd1306,_oled_device");
MODULE_ALIAS("of:N*T*Cssd1306,_oled_deviceC*");
MODULE_ALIAS("i2c:oled_device");

MODULE_INFO(srcversion, "ED077DCF196F398A0344427");
