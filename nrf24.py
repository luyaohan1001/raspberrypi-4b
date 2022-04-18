#!/usr/bin/python3
import time
import RPi.GPIO as GPIO

#一下试一下nrf24l01的C语言宏定义
TX_ADR_WIDTH = 5   	    # 5 uints TX address width
RX_ADR_WIDTH = 5   	    # 5 uints RX address width
TX_PLOAD_WIDTH = 32  	# 20 uints TX payload
RX_PLOAD_WIDTH = 32  	# 20 uints TX payload

#TX_ADDRESS   = 0x0909090909	#本地地址
#RX_ADDRESS   = 0x0909090909	#接收地址

TX_ADDRESS   = 0xE7E7E7E7E7	#本地地址
RX_ADDRESS   = 0xE7E7E7E7E7	#接收地址
R_REGISTER_MASK   = 0x00  	                    # 000A AAAA
W_REGISTER_MASK   = 0x20 	                    # 001A AAAA
RD_RX_PLOAD  = 0x61  	                    # 读取接收数据指令
WR_TX_PLOAD  = 0xA0  	                    # 写待发数据指令
FLUSH_TX     = 0xE1 	                    # 冲洗发送 FIFO指令
FLUSH_RX     = 0xE2  	                    # 冲洗接收 FIFO指令
REUSE_TX_PL  = 0xE3  	                    # 定义重复装载数据指令
NOP          = 0xFF  	                    # 保留
#*************************************SPI(nRF24L01)寄存器地址****************************************************
# Mnemonic   Address  Description
CONFIG       = 0x00  # 配置收发状态，CRC校验模式以及收发状态响应方式
EN_AA        = 0x01  # 自动应答功能设置
EN_RXADDR    = 0x02  # 可用信道设置
SETUP_AW     = 0x03  # 收发地址宽度设置
SETUP_RETR   = 0x04  # 自动重发功能设置
RF_CH        = 0x05  # 工作频率设置
RF_SETUP     = 0x06  # 发射速率、功耗功能设置
STATUS       = 0x07  # 状态寄存器
OBSERVE_TX   = 0x08  # 发送监测功能
CD           = 0x09  # 地址检测           
RX_ADDR_P0   = 0x0A  # 频道0接收数据地址
RX_ADDR_P1   = 0x0B  # 频道1接收数据地址
RX_ADDR_P2   = 0x0C  # 频道2接收数据地址
RX_ADDR_P3   = 0x0D  # 频道3接收数据地址
RX_ADDR_P4   = 0x0E  # 频道4接收数据地址
RX_ADDR_P5   = 0x0F  # 频道5接收数据地址
TX_ADDR      = 0x10  # 发送地址寄存器
RX_PW_P0     = 0x11  # 接收频道0接收数据长度
RX_PW_P1     = 0x12  # 接收频道0接收数据长度
RX_PW_P2     = 0x13  # 接收频道0接收数据长度
RX_PW_P3     = 0x14  # 接收频道0接收数据长度
RX_PW_P4     = 0x15  # 接收频道0接收数据长度
RX_PW_P5     = 0x16  # 接收频道0接收数据长度
FIFO_STATUS  = 0x17  # FIFO栈入栈出状态寄存器设置

TX_OK        = 0x20  #TX发送完成中断
MAX_TX       = 0x10  #达到最大发送次数中断


MOSI =  29
CSN  =  31
MISO =  33
SCK  =  35
CE   =  37
IRQ  =  32

# Pin Wiggling Macros:
def SPI_CS_1(): 
    GPIO.output(CSN, GPIO.LOW)
def SPI_CS_0():
    GPIO.output(CSN, GPIO.HIGH)
def SPI_SCK_1():
    GPIO.output(SCK, GPIO.HIGH)
def SPI_SCK_0():
    GPIO.output(SCK, GPIO.LOW)
def SPI_MOSI_1():
    GPIO.output(MOSI, GPIO.HIGH)
def SPI_MOSI_0():
    GPIO.output(MOSI, GPIO.LOW)
def SPI_CE_1():
    GPIO.output(CE, GPIO.HIGH)
def SPI_CE_0():
    GPIO.output(CE, GPIO.LOW)
def SPI_READ_MISO():
  return GPIO.input(MISO)
def SPI_READ_IRQ():
  return GPIO.input(IRQ)


def gpio_init(): 
  GPIO.setmode(GPIO.BOARD)
  GPIO.setwarnings(False)
  Pinlist = [29,31,35,37,11]
  GPIO.setup(Pinlist, GPIO.OUT)
  Pinlist_Input = [33,32]
  GPIO.setup(Pinlist_Input, GPIO.IN)

  SPI_CS_0()
  SPI_SCK_0()



# Brief: Time Sequence for SPI write single byte.
# Endianess: MSB. Cn: command bits. Sn: status register bits. Dn: data bits.
#
# CSN ````\___________________________________________________________________________________________________/````````
# MOSI______|C7|__|C6|__|C5|__|C4|__|C3|__|C2|__|C1|__|C0|______|D7|__|D6|__|D5|__|D4|__|D3|__|D2|__|D1|__|D0|
#           ^     ^     ^     ^     ^     ^     ^     ^         ^     ^     ^     ^     ^     ^     ^     ^  
# SCK ______/``\__/``\__/``\__/``\__/``\__/``\__/``\__/``\______/``\__/``\__/``\__/``\__/``\__/``\__/``\__/``\________
# MISO______|S7|__|S6|__|S5|__|S4|__|S3|__|S2|__|S1|__|S0|______XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX_________
#
# Pulse#     1     2     3     4     5     6     7     8         9     10    11    12    13    14   15     16
#
#
def gpio_clockout_8_bits(txData):
  spi_delay();
  for i in range (0,8):
      SPI_SCK_0();
      spi_delay()
      if(txData & 0x80): # MSB on each byte  
          SPI_MOSI_1()
      else:
          SPI_MOSI_0()
      SPI_SCK_1() # clock data
      txData = txData << 1
      spi_delay()
  SPI_SCK_0()


# Brief: Time Sequence for SPI read single byte.
# Endianess: MSB. Cn: command bits. Sn: status register bits. Dn: data bits.
#
# CSN ````\___________________________________________________________________________________________________/````````
# MOSI______|C7|__|C6|__|C5|__|C4|__|C3|__|C2|__|C1|__|C0|______|00|__|00|__|00|__|00|__|00|__|00|__|00|__|00|
#           ^     ^     ^     ^     ^     ^     ^     ^         ^     ^     ^     ^     ^     ^     ^     ^  
# SCK ______/``\__/``\__/``\__/``\__/``\__/``\__/``\__/``\______/``\__/``\__/``\__/``\__/``\__/``\__/``\__/``\____________
# MISO______|S7|__|S6|__|S5|__|S4|__|S3|__|S2|__|S1|__|S0|______|D0|__|D1|__|D2|__|D3|__|D4|__|D5|__|D6|__|D7|________ #
# Pulse#     1     2     3     4     5     6     7     8         9     10    11    12    13    14   15     16
def gpio_clockin_8_bits():
  rxData = 0
  spi_delay();
  for i in range (0,8):
      SPI_SCK_0();
      spi_delay()
      # SPI_MOSI_0() # dummy byte - dummy bit
      SPI_SCK_1()
      spi_delay()
      rxData = rxData << 1 # Why shift first then OR'? range (0, 8) will need to shift only 7 times.
      rxData |= SPI_READ_MISO()

      spi_delay()
  SPI_SCK_0()
  return rxData

  
def spi_delay():
	time.sleep(0.001)

def spi_write_register(reg, val, num_bytes=1):
  # Select chip
  SPI_CS_1()
  # Write chip register 
  gpio_clockout_8_bits(reg)
  # Write value
  for i in range(0, num_bytes):
    writing_byte = val & 0xff
    gpio_clockout_8_bits(writing_byte)
    val = val >> 8

  # Deselect chip
  SPI_CS_0()

def spi_read_register(reg, num_bytes=1):
  ret = 0

  # Select chip
  SPI_CS_1()
  # Write register address to read.
  gpio_clockout_8_bits(reg)
  # Read value
  for i in range(0, num_bytes):
    ret = ret << 8; 
    ret |= gpio_clockin_8_bits()

  # Deselect chip
  SPI_CS_0()
  return ret


def nrf24_poweron_self_test():
    config = spi_read_register(R_REGISTER_MASK + CONFIG, num_bytes=1)
    if (config != 0x08):
      print("(!) Critical Error: NRF24 CONFIG register should have reset value of 0x08. Re-plug in nrf24 on the 3.3V power wire.")
      print("CONFIG: " + hex(config))
    else:
      print("nrf24 poweron self test passed.")

def nrf24_rx_configure():
    SPI_CE_0();
    #spi_write_register(W_REGISTER_MASK + TX_ADDR, TX_ADDRESS, num_bytes=5 )      #  频道0自动	ACK应答允许
    #spi_write_register(W_REGISTER_MASK + RX_ADDR_P0, RX_ADDRESS, num_bytes=5 )      #  频道0自动	ACK应答允许
    spi_write_register(W_REGISTER_MASK+EN_AA, 0x00, num_bytes=1)      #  频道0自动	ACK应答允许
    spi_write_register(W_REGISTER_MASK+EN_RXADDR, 0x01, num_bytes=1)  #  允许接收地址只有频道0，如果需要多频道可以参考Page21
    spi_write_register(W_REGISTER_MASK + CONFIG, 0x0F)     

    rf_setup = spi_read_register(R_REGISTER_MASK + RF_SETUP, 1)
    print("rf_setup: " + str(hex(rf_setup)))
    SPI_CE_1();
    
    return 0

def nrf24_recive_packet():
    status = spi_read_register(R_REGISTER_MASK + STATUS, num_bytes=1)
    # SPI_CE_0()
    fifo_status = spi_read_register(R_REGISTER_MASK + FIFO_STATUS, num_bytes=1)
    # print("status: " + bin(status))
    #print("fifo status: " + bin(fifo_status))

    if (status & 0x40):

       packet = spi_read_register(RD_RX_PLOAD, 4)
       print("packet is: " + str(packet))
       print(packet)
       spi_write_register(W_REGISTER_MASK + STATUS, status, num_bytes=1)
   
    SPI_CE_1()


# main
gpio_init()
nrf24_poweron_self_test()
nrf24_rx_configure()

while True:
  nrf24_recive_packet()


