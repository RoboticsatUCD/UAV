#Evan Racah
#9/18/2013
#Initialize IMU object to be used from this module
from sensor_class import Sensor
from I2C_Class import *
from registers import *
from robovero.extras import Array, roboveroConfig, IMUInit
from robovero.lpc17xx_i2c import I2C_M_SETUP_Type, I2C_MasterTransferData, \
                            I2C_TRANSFER_OPT_Type
from robovero.lpc17xx_gpio import GPIO_ReadValue
from robovero.LPC17xx import LPC_I2C0
from robovero.lpc_types import Status
import time

#(self,sensor_type,address,registers,offset,bits,sensitivity,max_voltage):
gyro_addr=0x68
accel_addr=0x18
compass_addr=0x1E

# Initialize pin select registers
roboveroConfig()

# Initialize IMU
IMUInit()

#registers is list of three tuples for registers [(xlow,xhigh),(ylow,yhigh), etc]
gyro_regs=[(gyro_x_low,gyro_x_high),(gyro_y_low,gyro_y_high),(gyro_z_low,gyro_z_high)]
accel_regs=[(accel_x_low,accel_x_high),(accel_y_low,accel_y_high),(accel_z_low,accel_z_high)]
offsets=(-118,-551,910)
accel=Sensor("accel",accel_addr,accel_regs,offsets,16,0)
accel.writeReg(accel_ctrl_reg1, 0x27)
accel.writeReg(accel_ctrl_reg4, 0x00)
#todo create inherited classes for gyro, compass, accel_addr
while(1):
	print "x: ",accel.xRaw
	print "y: ",accel.yRaw
	print "z: ",accel.zRaw
	
