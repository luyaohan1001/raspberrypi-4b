/**
 * @file datalink.c
 * @brief Datalink layer implementation for SSD1306 OLED Driver, SMBus-based operations.
*/

#include <linux/module.h>
#include <linux/init.h>
#include <linux/i2c.h>
#include "datalink.h"

/* SSD1306 I2C command table. */
#define SET_MEMORY_ADDRESSING_MODE  0x20
#define SET_DISPLAY_START_LINE      0x40
#define SET_DISPLAY_OFF             0xAE
#define SET_DISPLAY_ON              0xAF
#define SET_ENTIRE_DISPLAY_ON       0xA4
#define SET_DISPLAY_OFFSET          0xD3
#define SET_MUX_RATIO               0xA8
#define SET_DEACTIVATE_SCROLL       0x2E
#define SET_CONTRAST_CONTROL        0x81
#define SET_CHARGE_PUMP             0x8D
#define SET_CHARGE_PUMP_ENABLE      0x14

#define DUMMY_DATA                  0x00

/* Global symbol to the i2c client instance. */
extern struct i2c_client *i2c_client;

void ssd1306_configure(uint8_t command, eParam_t PARAM_OPTION, uint8_t param)
{
  ssd1306_packet_t packet = {
    .control_byte0 = 0x00,
    .command = command,
    .control_byte1 = 0x00,
    .param = param,
  };

  if (PARAM_OPTION == HAS_PARAM) {
    i2c_master_send(i2c_client, (uint8_t *)&packet, 4);
  } else if (PARAM_OPTION == NO_PARAM) {
    i2c_master_send(i2c_client, (uint8_t *)&packet, 2);
  }
}


int ssd1306_display_init(void)
{
  ssd1306_configure(SET_DISPLAY_OFF, NO_PARAM, DUMMY_DATA); // Entire Display OFF

  ssd1306_configure(SET_DISPLAY_OFFSET, HAS_PARAM, 0x00); // Set display offset

  ssd1306_configure(SET_DISPLAY_START_LINE, NO_PARAM, DUMMY_DATA); // Set first line as the start line of the display

  ssd1306_configure(SET_CHARGE_PUMP, NO_PARAM, DUMMY_DATA); 

  ssd1306_configure(SET_CHARGE_PUMP_ENABLE, NO_PARAM, DUMMY_DATA); 

  ssd1306_configure(SET_MEMORY_ADDRESSING_MODE, HAS_PARAM, 0x00); // Set memory addressing mode

  ssd1306_configure(SET_CONTRAST_CONTROL, HAS_PARAM, 0x80); // Set contrast control

  ssd1306_configure(SET_ENTIRE_DISPLAY_ON, NO_PARAM, DUMMY_DATA); // Entire display ON, resume to RAM content display

  ssd1306_configure(SET_DISPLAY_ON, NO_PARAM, DUMMY_DATA); // Set Display in Normal Mode, 1 = ON, 0 = OFF

  ssd1306_configure(SET_DEACTIVATE_SCROLL, NO_PARAM, DUMMY_DATA); // Deactivate scroll

  ssd1306_configure(SET_DISPLAY_ON, NO_PARAM, DUMMY_DATA); // Display ON in normal mode
  
  // Clear the display
  // SSD1306_Fill(0x00);
  return 0;
}