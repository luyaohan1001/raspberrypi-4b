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
	{ 0xaa68f632, "misc_register" },
	{ 0x1b16b90, "misc_deregister" },
	{ 0xc5850110, "printk" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("of:N*T*Carrow,hellokeys");
MODULE_ALIAS("of:N*T*Carrow,hellokeysC*");

MODULE_INFO(srcversion, "0AC48761D605B5BC530BEA3");
