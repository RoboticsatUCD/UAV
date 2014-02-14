#Evan Racah
#9/18/2013
#Initialize IMU object to be used from this module
from imu import IMU
from robovero.extras import roboveroConfig
import time
from ComplementaryFilter import ComplementaryFilter
#from motor import Motor
from PID import PIDControl


roboveroConfig()

# Initialize IMU
imu = IMU()
#imu.calibrate(0, 0, -1)
cfRoll = ComplementaryFilter(0.9, 0)
cfPitch = ComplementaryFilter(0.9, 0)
"""
motor1 = Motor(1)
motor2 = Motor(2)
motor3 = Motor(5)
motor4 = Motor(4)
"""
#pidPitch = PIDControl(0, 1)
#pidRoll = PIDControl(0, 1)

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





