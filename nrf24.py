#!/usr/bin/python3
import time
import RPi.GPIO as GPIO

#一下试一下nrf24l01的C语言宏定义
TX_ADR_WIDTH = 5   	    # 5 uints TX address width
RX_ADR_WIDTH = 5   	    # 5 uints RX address width
TX_PLOAD_WIDTH = 32  	# 20 uints TX payload
RX_PLOAD_WIDTH = 32  	# 20 uints TX payload

TX_ADDRESS   = [0x09,0x09,0x09,0x09,0x09]	#本地地址
RX_ADDRESS   = [0x09,0x09,0x09,0x09,0x09]	#接收地址
READ_REG     = 0x00  	                    # 读寄存器指令
WRITE_REG    = 0x20 	                    # 写寄存器指令
RD_RX_PLOAD  = 0x61  	                    # 读取接收数据指令
WR_TX_PLOAD  = 0xA0  	                    # 写待发数据指令
FLUSH_TX     = 0xE1 	                    # 冲洗发送 FIFO指令
FLUSH_RX     = 0xE2  	                    # 冲洗接收 FIFO指令
REUSE_TX_PL  = 0xE3  	                    # 定义重复装载数据指令
NOP          = 0xFF  	                    # 保留
#*************************************SPI(nRF24L01)寄存器地址****************************************************
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


def SPI_IoInit(): 
  GPIO.setmode(GPIO.BOARD)
  GPIO.setwarnings(False)
  Pinlist = [29,31,35,37,11]
  GPIO.setup(Pinlist, GPIO.OUT)
  Pinlist_Input = [33,32]
  GPIO.setup(Pinlist_Input, GPIO.IN)

  SPI_CS_1()
  SPI_SCK_0()

def spi_delay():
	time.sleep(0.001)


# Brief: Time Sequence for SPI write single byte.
# Endianess: MSB. Cn: command bits. Sn: status register bits. Dn: data bits.
#
# CSN ````\___________________________________________________________________________________________________/````````
# MOSI______|C7|__|C6|__|C5|__|C4|__|C3|__|C2|__|C1|__|C0|______|D7|__|D6|__|D5|__|D4|__|D3|__|D2|__|D1|__|D0|
#           ^     ^     ^     ^     ^     ^     ^     ^         ^     ^     ^     ^     ^     ^     ^     ^  
# SCK ______/``\__/``\__/``\__/``\__/``\__/``\__/``\__/``\______/``\__/``\__/``\__/``\__/``\__/``\__/``\__/``\____________
# MISO______|S7|__|S6|__|S5|__|S4|__|S3|__|S2|__|S1|__|S0|______XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX________
#
# Pulse#     1     2     3     4     5     6     7     8         9     10    11    12    13    14   15     16
#
#
def SPI_WriteByte(txData):
  spi_delay();
  for i in range (0,8):
      SPI_SCK_0();
      spi_delay()
      if(txData & 0x80): # MSB on each byte first
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
def SPI_ReadByte():
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

def SPI_WR_Reg(reg, val):
  SPI_CS_1()
  SPI_CE_1()
  SPI_WriteByte(reg)
  SPI_WriteByte(val)
  SPI_CS_0()
  SPI_CE_0()

def SPI_RD_Reg(reg):
  SPI_CS_1()
  SPI_CE_1()
  SPI_WriteByte(reg)
  status =  SPI_ReadByte()
  SPI_CS_0()
  SPI_CE_0()
  return status

def Init_NRF24L01():
    SPI_WR_Reg(EN_AA, 0x01)      #  频道0自动	ACK应答允许
    SPI_WR_Reg(EN_RXADDR, 0x01)  #  允许接收地址只有频道0，如果需要多频道可以参考Page21
    SPI_WR_Reg(RF_CH, 40)        #   设置信道工作为2.4GHZ，收发必须一致
    SPI_WR_Reg(RX_PW_P0, RX_PLOAD_WIDTH) #设置接收数据长度，本次设置为32字节
    SPI_WR_Reg(RF_SETUP, 0x0f)   		#设置发射速率为1MHZ，发射功率为最大值0dB
    return 0

STATUS       = 0x07  # 状态寄存器
SPI_IoInit()
status=SPI_RD_Reg(STATUS)
print(status)
#
# Init_NRF24L01()
enaa=SPI_RD_Reg(0x01)
print(enaa)


