#include <linux/module.h>
#include <linux/init.h>
#include <linux/proc_fs.h>
#include <linux/i2c.h>
#include <linux/delay.h>


extern struct i2c_client *oled_client;


int I2C_Write(unsigned char *buf, unsigned int len)
{
  /*
  ** Sending Start condition, Slave address with R/W bit, 
  ** ACK/NACK and Stop condtions will be handled internally.
  */ 
  int ret = i2c_master_send(oled_client, buf, len);
  
  return ret;
}

void SSD1306_Write(bool is_cmd, unsigned char data)
{
  unsigned char buf[2] = {0};
  int ret;
  
  /*
  ** First byte is always control byte. Data is followed after that.
  **
  ** There are two types of data in SSD_1306 OLED.
  ** 1. Command
  ** 2. Data
  **
  ** Control byte decides that the next byte is, command or data.
  **
  ** -------------------------------------------------------                        
  ** |              Control byte's | 6th bit  |   7th bit  |
  ** |-----------------------------|----------|------------|    
  ** |   Command                   |   0      |     0      |
  ** |-----------------------------|----------|------------|
  ** |   data                      |   1      |     0      |
  ** |-----------------------------|----------|------------|
  ** 
  ** Please refer the datasheet for more information. 
  **    
  */ 
  if( is_cmd == true )
  {
      buf[0] = 0x00;
  }
  else
  {
      buf[0] = 0x40;
  }
  
  buf[1] = data;
  
  ret = I2C_Write(buf, 2);
}



int SSD1306_DisplayInit(void)
{
  msleep(100);               // delay

  /*
  ** Commands to initialize the SSD_1306 OLED Display
  */
  SSD1306_Write(true, 0xAE); // Entire Display OFF
  SSD1306_Write(true, 0xD5); // Set Display Clock Divide Ratio and Oscillator Frequency
  SSD1306_Write(true, 0x80); // Default Setting for Display Clock Divide Ratio and Oscillator Frequency that is recommended
  SSD1306_Write(true, 0xA8); // Set Multiplex Ratio
  SSD1306_Write(true, 0x3F); // 64 COM lines
  SSD1306_Write(true, 0xD3); // Set display offset
  SSD1306_Write(true, 0x00); // 0 offset
  SSD1306_Write(true, 0x40); // Set first line as the start line of the display
  SSD1306_Write(true, 0x8D); // Charge pump
  SSD1306_Write(true, 0x14); // Enable charge dump during display on
  SSD1306_Write(true, 0x20); // Set memory addressing mode
  SSD1306_Write(true, 0x00); // Horizontal addressing mode
  SSD1306_Write(true, 0xA1); // Set segment remap with column address 127 mapped to segment 0
  SSD1306_Write(true, 0xC8); // Set com output scan direction, scan from com63 to com 0
  SSD1306_Write(true, 0xDA); // Set com pins hardware configuration
  SSD1306_Write(true, 0x12); // Alternative com pin configuration, disable com left/right remap
  SSD1306_Write(true, 0x81); // Set contrast control
  SSD1306_Write(true, 0x80); // Set Contrast to 128
  SSD1306_Write(true, 0xD9); // Set pre-charge period
  SSD1306_Write(true, 0xF1); // Phase 1 period of 15 DCLK, Phase 2 period of 1 DCLK
  SSD1306_Write(true, 0xDB); // Set Vcomh deselect level
  SSD1306_Write(true, 0x20); // Vcomh deselect level ~ 0.77 Vcc
  SSD1306_Write(true, 0xA4); // Entire display ON, resume to RAM content display
  SSD1306_Write(true, 0xA6); // Set Display in Normal Mode, 1 = ON, 0 = OFF
  SSD1306_Write(true, 0x2E); // Deactivate scroll
  SSD1306_Write(true, 0xAF); // Display ON in normal mode
  
  //Clear the display
  // SSD1306_Fill(0x00);
  return 0;
}

