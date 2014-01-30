#Evan Racah
#9/18/2013
#Initialize IMU object to be used from this module
from imu import IMU
from robovero.extras import roboveroConfig
import time



#set addresses for each sensor


# Initialize pin select registers
roboveroConfig()

# Initialize IMU
imu=IMU()

#registers is list of three tuples for registers [(xlow,xhigh),(ylow,yhigh), etc]

while(1):
	print "Roll: ", imu.roll_angle()
	print "Pitch: ",imu.pitch_angle()
	print "Roll rate: ", imu.roll_rate()
	print "Pitch rate: ",imu.pitch_rate()
	
	time.sleep(0.5)

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
