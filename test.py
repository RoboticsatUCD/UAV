#Evan Racah
#test.py

from robovero.extras import roboveroConfig
from imu_class import IMU
from registers import gyro_offsets
#from gyro_class import Gyroscope
from registers import accel_offsets
from accel_class import Accelerometer
import time
from complementary_filter import *


roboveroConfig()

time_step = 10./1000.

myIMU=IMU()

while(1):
	t1 = time.time()
	print myIMU.roll_angle
	print myIMU.pitch_angle
	t2 = time.time()
	print "time: ", t2-t1

"""
while(1):
	print "roll", myIMU.roll_rate
	print "pitch", myIMU.pitch_rate
	
"""

#instantiates complimetary filters for both pitch and roll angle, initial
#angle is just angle that accel outputs
#pitch_filter=ComplementaryFilter(0.7,myIMU.pitch_angle,time_step)
  
#roll_filter=ComplementaryFilter(0.7,myIMU.roll_angle,time_step)

"""
def test_loop():
	while(1):
		#t1=time.clock()
		pitch=pitch_filter.filter(myIMU.pitch_angle,myIMU.pitch_rate)
		roll=roll_filter.filter(myIMU.roll_angle,myIMU.roll_rate)
		#t2=time.clock()
		#print "time: ", t2-t1
		print "roll angle: %f \n pitch angle %f" %(roll,pitch)
		
"""

#main



#test_loop()


"""
gyro=Gyroscope(gyro_offsets)
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

#		print "x: ",x
#		print "y: ",y
#		print "z: ",z

		x_tot+=x
		y_tot+=y
		z_tot+=z

		count+=1

		time.sleep(0.1)

	print "x avg: ",x_tot/count
	print "y avg: ",y_tot/count
	print "z avg: ",z_tot/count

find_offset(gyro)
"""
