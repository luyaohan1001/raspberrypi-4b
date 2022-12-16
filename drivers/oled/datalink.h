#include <linux/module.h>
#include <linux/init.h>
#include <linux/i2c.h>
#include <linux/delay.h>

typedef struct {
    uint8_t control_byte0;
    uint8_t command;
    uint8_t control_byte1;
    uint8_t param;
} ssd1306_packet_t;

typedef enum {
    HAS_PARAM,
    NO_PARAM,
} eParam_t;

void ssd1306_configure(uint8_t command, eParam_t PARAM_OPTION, uint8_t param);
int ssd1306_display_init(void);
