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

#sta = 0
#RX_DR = 0
#树莓派各个引脚的定义
MOSI =  29
CSN  =  31
MISO =  33
SCK  =  35
CE   =  37
IRQ  =  32
def GPIO_Init():
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setwarnings(False)
    Pinlist = [29,31,35,37,11]
    GPIO.setup(Pinlist, GPIO.OUT)
    Pinlist_Input = [33,32]
    GPIO.setup(Pinlist_Input, GPIO.IN)
    return 0

def LEDH():
    GPIO.output(11, GPIO.HIGH)

def LEDL():
    GPIO.output(11, GPIO.LOW)

#****************************************************************************************************
#*函数：uint SPI_RW(uint dat)
#*功能：NRF24L01的SPI写时序
#****************************************************************************************************
def SPI_RW(dat):
    bit_ctr = 8
    _MOSI   = 0
    while(bit_ctr):

        bit_ctr = bit_ctr - 1
        _MOSI = dat & 0x80              #output 'dat', MSB to MOSI
        if(_MOSI):
            GPIO.output(MOSI, GPIO.HIGH)
        else:
            GPIO.output(MOSI, GPIO.LOW)
        dat = (dat << 1)                #shift next bit into MSB..
        GPIO.output(SCK, GPIO.HIGH)          #Set SCK GPIO.high..
        dat |= GPIO.input(MISO)        #capture current MISO bit
        GPIO.output(SCK, GPIO.LOW)           #..then set SCK GPIO.low again
    return dat           		        #return read dat

#****************************************************************************************************
#*函数：uchar SPI_Read(uchar reg)
#*功能：NRF24L01的SPI读时序
#*****************************************************************************************************
def SPI_Read(reg):
    reg_val = 0
    GPIO.output(CSN, GPIO.LOW)              #CSN GPIO.low, initialize SPI communication...
    SPI_RW(reg)                         #Select register to read from..
    reg_val = SPI_RW(0)                 #..then read registervalue
    GPIO.output(CSN, GPIO.HIGH)             #CSN GPIO.high, terminate SPI communication
    return reg_val                      #return register value

#****************************************************************************************************#
#*功能：NRF24L01读写寄存器函数
#****************************************************************************************************#
def SPI_RW_Reg(reg,value):
    status = 0
    GPIO.output(CSN, GPIO.LOW)              #CSN GPIO.low, init SPI transaction
    status = SPI_RW(reg)                #select register
    SPI_RW(value)                       #..and write value to it..
    GPIO.output(CSN, GPIO.HIGH)             #CSN GPIO.high again
    return status                       #return nRF24L01 status uchar

#****************************************************************************************************#
#*函数：uint SPI_Read_Buf(uchar reg, uchar *pBuf, uchar uchars)
#*功能: 用于读数据，reg：为寄存器地址，pBuf：为待读出数据地址，uchars：读出数据的个数
#****************************************************************************************************#
def SPI_Read_Buf(reg, pBuf, uchars):
    status    = 0
    uchar_ctr = 0
    GPIO.output(CSN, GPIO.LOW)                    		# Set CSN GPIO.low, init SPI tranaction
    status = SPI_RW(reg)       		    # Select register to write to and read status uchar
    while(uchar_ctr < uchars): 
        pBuf[uchar_ctr] = SPI_RW(0)     #
        uchar_ctr = uchar_ctr + 1 
    GPIO.output(CSN, GPIO.HIGH)                           
    return(status)                      #return nRF24L01 status uchar

#*********************************************************************************************************
#*函数：uint SPI_Write_Buf(uchar reg, uchar *pBuf, uchar uchars)
#*功能: 用于写数据：为寄存器地址，pBuf：为待写入数据地址，uchars：写入数据的个数
#*********************************************************************************************************#
def SPI_Write_Buf(reg, pBuf, uchars):
    status = 0
    uchar_ctr = 0	
    GPIO.output(CSN, GPIO.LOW)           #SPI使能       
    status = SPI_RW(reg)   
    while(uchar_ctr < uchars): #
        SPI_RW(pBuf[uchar_ctr])
        uchar_ctr = uchar_ctr + 1
    GPIO.output(CSN, GPIO.HIGH)           #关闭SPI
    return(status)


#****************************************************************************************************#
#*函数：void SetRX_Mode(void)
#*功能：数据接收配置 
#****************************************************************************************************#
def SetRX_Mode():
	GPIO.output(CE, GPIO.LOW)
	SPI_RW_Reg(WRITE_REG + CONFIG, 0x0f)   		# IRQ收发完成中断响应，16位CRC	，主接收
	GPIO.output(CE, GPIO.HIGH) 


#******************************************************************************************************#
#*函数：unsigned char nRF24L01_RxPacket(unsigned char* rx_buf)
#*功能：数据读取后放如rx_buf接收缓冲区中
#******************************************************************************************************#
def nRF24L01_RxPacket(rx_buf):

    revale = 0
    sta = 0
    RX_DR = 0
    sta = SPI_Read(STATUS)	                                # 读取状态寄存其来判断数据接收状况
    # RX_DR = sta&0x40
    #RX_DR = sta&
    print(sta)
    if(RX_DR):				                                # 判断是否接收到数据
        GPIO.output(CE, GPIO.LOW) 			                #SPI使能
        SPI_Read_Buf(RD_RX_PLOAD,rx_buf,TX_PLOAD_WIDTH)     # read receive payload from RX_FIFO buffer
        revale =1			                                #读取数据完成标志
    SPI_RW_Reg(WRITE_REG+STATUS,sta)                        #接收到数据后RX_DR,TX_DS,MAX_PT都置高为1，通过写1来清楚中断标志
    return revale


#***********************************************************************************************************
#*函数：void nRF24L01_TxPacket(unsigned char * tx_buf)
#*功能：发送 tx_buf中数据
#**********************************************************************************************************#
def nRF24L01_TxPacket(tx_buf):
    sta = 0
    GPIO.output(CE, GPIO.LOW)
    SPI_RW_Reg(WRITE_REG + CONFIG, 0x0e)
    GPIO.output(CE, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(CE, GPIO.LOW)			                        #StandBy I模式	
    SPI_Write_Buf(WR_TX_PLOAD, tx_buf, TX_PLOAD_WIDTH) 			# 装载数据	
    GPIO.output(CE, GPIO.HIGH)		                            #置高CE，激发数据发送
#	while(GPIO.input(IRQ)!=0)                                   #等待发送完成
    sta=SPI_Read(STATUS)		   
    if(sta & MAX_TX):                                           #达到最大重发次数
        SPI_RW_Reg(FLUSH_TX,0xff)                               #清除TX FIFO寄存器
        return MAX_TX
        
    if(sta&TX_OK):                                              #发送完成
        return 0
	
    return 0xff                                                 #其他原因发送失败


#****************************************************************************************
#*NRF24L01初始化
#***************************************************************************************#
def Init_NRF24L01():
    GPIO.output(CE, GPIO.LOW)    # chip enable
    GPIO.output(CSN, GPIO.HIGH)   # Spi disable 
    GPIO.output(SCK, GPIO.LOW)   # Spi clock line init GPIO.high
    SPI_Write_Buf(WRITE_REG + TX_ADDR, TX_ADDRESS, TX_ADR_WIDTH)    # 写本地地址	
    SPI_Write_Buf(WRITE_REG + RX_ADDR_P0, RX_ADDRESS, RX_ADR_WIDTH) # 写接收端地址
    SPI_RW_Reg(WRITE_REG + EN_AA, 0x01)      #  频道0自动	ACK应答允许	
    SPI_RW_Reg(WRITE_REG + EN_RXADDR, 0x01)  #  允许接收地址只有频道0，如果需要多频道可以参考Page21  
    SPI_RW_Reg(WRITE_REG + RF_CH, 40)        #   设置信道工作为2.4GHZ，收发必须一致
    SPI_RW_Reg(WRITE_REG + RX_PW_P0, RX_PLOAD_WIDTH) #设置接收数据长度，本次设置为32字节
    SPI_RW_Reg(WRITE_REG + RF_SETUP, 0x0f)   		#设置发射速率为1MHZ，发射功率为最大值0dB
    return 0

def spi_test():
    GPIO.output(CE, GPIO.LOW)    # chip enable
    GPIO.output(CSN, GPIO.HIGH)   # Spi disable 
    GPIO.output(SCK, GPIO.LOW)   # Spi clock line init GPIO.high
    SPI_Write_Buf(WRITE_REG + TX_ADDR, TX_ADDRESS, TX_ADR_WIDTH)    # 写本地地址	
    TxBuf = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    SPI_Read_Buf(WRITE_REG + TX_ADDR, TxBuf, TX_ADR_WIDTH)    # 写本地地址	
    print(TxBuf)



if __name__ == "__main__":
    TxBuf = [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0]
    RxBuf = [0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0]
    GPIO_Init()

    spi_test()
    quit()

    # Init_NRF24L01()
    # SetRX_Mode()
    while True:
        if nRF24L01_RxPacket(RxBuf):
            if RxBuf[0]:
                print(RxBuf)
                LEDH()
                SetRX_Mode()
            time.sleep(1)
            LEDL()
            time.sleep(1)
