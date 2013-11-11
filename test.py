#Evan Racah
#test.py
from robovero.extras import roboveroConfig
from imu_class import IMU
from accel_class import Accelerometer
from registers import accel_offsets
import time
from complementary_filter import *


print "0"
roboveroConfig()

time_step=10./1000.
print "0.1"
myIMU=IMU()  #instantiate IMU -> it does not take any data
print "1"
#instantiates complimetary filters for both pitch and roll angle, initial
#angle is just angle that accel outputs
pitch_filter=ComplemetaryFilter(0,myIMU.pitch_angle,time_step)
print "2"  
roll_filter=ComplemetaryFilter(0,myIMU.roll_angle,time_step)
print "3"

def test_loop():
	while(1):
		pitch=pitch_filter.filter(myIMU.pitch_angle,myIMU.pitch_rate)
		roll=roll_filter.filter(myIMU.roll_angle,myIMU.roll_rate)
		print "roll angle: %f \n pitch angle %f" %(roll,pitch)
		time.sleep(time_step)


#main


print "4"
test_loop()

"""
accel=Accelerometer(accel_offsets)
def find_offset(sensor):
	count=0
	x_tot=0
	y_tot=0
	z_tot=0

	while(count<100):
		x=sensor.xRaw
		y=sensor.yRaw
		z=sensor.zRaw
#		print "x: ",x
#		print "y: ",y
#		print "z: ",z
		x_tot+=x
		y_tot+=y
		z_tot+=z

		count+=1
	print "x avg: ",x_tot/count
	print "y avg: ",y_tot/count
	print "z avg: ",z_tot/count

find_offset(accel)
"""
