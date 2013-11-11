#Evan Racah
#9/18/2013
#Initialize IMU object to be used from this module
from sensor_class import Sensor
from imu_class import IMU
from I2C_Class import *
from registers import *
from robovero.extras import Array, roboveroConfig
from robovero.lpc17xx_i2c import I2C_M_SETUP_Type, I2C_MasterTransferData, \
                            I2C_TRANSFER_OPT_Type
from robovero.lpc17xx_gpio import GPIO_ReadValue
from robovero.LPC17xx import LPC_I2C0
from robovero.lpc_types import Status
import time



#set addresses for each sensor
gyro_addr=0x68
accel_addr=0x18
compass_addr=0x1E

# Initialize pin select registers
roboveroConfig()

# Initialize IMU


#registers is list of three tuples for registers [(xlow,xhigh),(ylow,yhigh), etc]

accel_regs=[(accel_x_low,accel_x_high),(accel_y_low,accel_y_high),(accel_z_low,accel_z_high)]
accel_offsets=(-118,-551,910)
gyro_offsets=(-118,-551,910)
#(self,sensor_type,address,registers,offset,bits,sensitivity,max_voltage):
accel=Sensor("accel",accel_addr,accel_regs,accel_offsets,16,0)
accel.writeReg(accel_ctrl_reg1, 0x27)
accel.writeReg(accel_ctrl_reg4, 0x00)


gyro=Sensor("gyro",gyro_addr,gyro_regs,gyro_offsets,16,0)
gyro.writeReg(gyro_ctrl_reg3, 0x08) # enable DRDY
gyro.writeReg(gyro_ctrl_reg4, 0x80) # enable block data read mode
gyro.writeReg(gyro_ctrl_reg1, 0x0F) # normal mode, enable all axes, 250dps
#todo create inherited classes for gyro, compass, accel

imu=IMU(accel,gyro)



"""
while(1):
	print "Roll: ",imu.roll_angle
	print "Pitch: ",imu.pitch_angle
	time.sleep(1)"""

def find_offset(sensor):
	count=0
	x_tot=0
	y_tot=0
	z_tot=0

	while(count<100):
		x=sensor.xRaw
		y=sensor.yRaw
		z=sensor.zRaw
		print "x: ",x
		print "y: ",y
		print "z: ",z
		x_tot+=x
		y_tot+=y
		z_tot+=z

		count+=1
		time.sleep(0.1)
	print "x avg: ",x_tot/count
	print "y avg: ",y_tot/count
	print "z avg: ",z_tot/count

find_offset()

