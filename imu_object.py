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


# Initialize pin select registers
roboveroConfig()

# Initialize IMU


#registers is list of three tuples for registers [(xlow,xhigh),(ylow,yhigh), etc]

imu=IMU()




while(1):
	print "Roll: ",imu.roll_angle
	print "Pitch: ",imu.pitch_angle
	time.sleep(1)

"""
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

"""