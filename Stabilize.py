'''
Created on Aug 15, 2013

@author: ejracah
'''

"""from imu import IMU
from sensor_class import Sensor"""

from imu import IMU
from robovero.extras import roboveroConfig
import time
from ComplementaryFilter import ComplementaryFilter
from motor import Motor
from PID import PIDControl
import signal
import sys

roboveroConfig()

# Initialize IMU
imu = IMU()
#imu.calibrate(0, 0, -1)
cfRoll = ComplementaryFilter(0.9, 0)
cfPitch = ComplementaryFilter(0.9, 0)

motor1 = Motor(1)
motor2 = Motor(6)
motor3 = Motor(5)
motor4 = Motor(4)
motors = [motor1, motor2, motor3, motor4]

pitchPID = PIDControl(0, 0.168, 0.654 ,0.008)
rollPID = PIDControl(0, 0.168, 0.654 ,0.008)

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)
    for m in motors:
    	mot.setSpeed(0)
    	mot.go()
signal.signal(signal.SIGINT, signal_handler)


while(1):
	rollAngle = cfRoll.filter(imu.roll_angle, imu.roll_rate)
	pitchAngle = cfPitch.filter(imu.pitch_angle, imu.pitch_rate)
	
	pitchU = (pitchPID.update(pitchAngle) / 2)
	rollU = (rollPID.update(rollAngle) / 2)
	
	throttle = 200
	#Set motor speeds
	motor1.setSpeed(throttle + pitchU)
	motor2.setSpeed(throttle + rollU)
	motor3.setSpeed(throttle - pitchU)
	motor4.setSpeed(throttle - rollU)

	print "pitchU: ", pitchU, " rollU: " , rollU
	print "pitch angle: ", pitchAngle, " roll angle: " , rollAngle
	

	#Start Motors
	for mot in motors:
	    mot.go()

	time.sleep(0.001)


