#Evan Racah
#test.py
from robovero.extras import roboveroConfig
from imu_class import IMU
from accel_class import Accelerometer
from registers import accel_offsets
import time
#myIMU=IMU()  #instantiate IMU -> it does not take any data


print "hey_1"
roboveroConfig()
print "hey_2"
accel=Accelerometer(accel_offsets)
print "hey_test"
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
print "hey_test2"
find_offset(accel)
print "hey_test3"