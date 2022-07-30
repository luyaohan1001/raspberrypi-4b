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
	{ 0x40e518c8, "platform_driver_unregister" },
	{ 0x5af58d5d, "__platform_driver_register" },
	{ 0x86332725, "__stack_chk_fail" },
	{ 0x86bc4e00, "device_property_read_u32_array" },
	{ 0xd2df0409, "device_property_read_string" },
	{ 0x2d76c278, "device_property_present" },
	{ 0x8f678b07, "__stack_chk_guard" },
	{ 0xc5850110, "printk" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("of:N*T*Cbrightlight,_mydev");
MODULE_ALIAS("of:N*T*Cbrightlight,_mydevC*");

MODULE_INFO(srcversion, "00C8265B15EBFADA5FC27D2");
