#include <linux/module.h>
#include <linux/init.h>
#include <linux/proc_fs.h>
#include <linux/i2c.h>
#include <linux/delay.h>

int I2C_Write(unsigned char *buf, unsigned int len);

void SSD1306_Write(bool is_cmd, unsigned char data);

int SSD1306_DisplayInit(void);

