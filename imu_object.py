#Evan Racah
#9/18/2013
#Initialize IMU object to be used from this module
from sensor_class import Sensor
from kalman_lib import *
#(self,sensor_type,address,registers,offset,bits,sensitivity,max_voltage):
gyro_addr=0x68
accel_addr=0x18
compass_addr=0x1E
#registers is list of three tuples for registers [(xlow,xhigh),(ylow,yhigh), etc]
gyro_regs=[(gyro_x_low,gyro_x_high)]
gyro=Sensor("gyro",gyro_addr)
#todo create inherited classes for gyro, compass, accel_addr