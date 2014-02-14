#Evan Racah
#9/18/2013
#Initialize IMU object to be used from this module
from imu import IMU
from robovero.extras import roboveroConfig
import time
from ComplementaryFilter import ComplementaryFilter
from motor import Motor
from PID import PIDControl


roboveroConfig()

# Initialize IMU
imu=IMU()
#imu.calibrate(0, 0, -1)
cfRoll=ComplementaryFilter()
cfPitch=ComplementaryFilter()
motor1 = Motor(1)
motor2 = Motor(2)
motor3 = Motor(5)
motor4 = Motor(4)
pidPitch = PIDControl(0, 1)
pidRoll = PIDControl(0, 1)

#registers is list of three tuples for registers [(xlow,xhigh),(ylow,yhigh), etc]
string = ""

while(1):
	string = "Roll: " + str(imu.roll_angle)
	string += "\nPitch: " + str(imu.pitch_angle)
	string += "\nRoll rate: " + str(imu.roll_rate)
	string += "\nPitch rate: " + str(imu.pitch_rate)
	string += "\nfrom filter Roll: " + str(cfRoll.filter(imu.roll_angle, imu.roll_rate))
	string += "\nfrom filter Pitch: " + str(cfPitch.filter(imu.pitch_angle, imu.pitch_rate)) 
	print string

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
