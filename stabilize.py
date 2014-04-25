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
import thread

roboveroConfig()

# Initialize IMU
imu = IMU()

#imu.calibrate(0, 0, -1)
cfRoll = ComplementaryFilter(0.9, 0)
cfPitch = ComplementaryFilter(0.9, 0)

#motor1 = Motor(5)
#motor2 = Motor(6)
motor3 = Motor(1)
#motor4 = Motor(4)
motors = [motor3]

for m in motors:
   m.setSpeed(1000)
   m.go()
   time.sleep(1)
   m.setSpeed(0)
   m.go()


pitchPID = PIDControl(0, [0.168, 0.654 ,0.008])
#rollPID = PIDControl(0, [1, 0 ,0])

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    for m in motors:
        m.setSpeed(0)
        m.go()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def getInput(PIDControl):
	angle = 0
	while(1):
		angle = raw_input('Set desired angle: ')
		PIDControl.set_set_point(int(angle))
try:
	thread.start_new_thread(getInput, (pitchPID, ))
except:
	print "error: unable to start thread"

while(1):
#	rollAngle = cfRoll.filter(imu.roll_angle, imu.roll_rate)
	pitchAngle = cfPitch.filter(imu.pitch_angle, imu.pitch_rate)
	
	pitchU = (pitchPID.update(pitchAngle))
#	rollU = (rollPID.update(rollAngle))
	
	throttle = 400
	#Set motor speeds
	#motor1.setSpeed(throttle + pitchU)
	#motor2.setSpeed(throttle + rollU)
	motor3.setSpeed(throttle - pitchU)
	#motor4.setSpeed(throttle - rollU)

#	print "pitchU: ", pitchU, " rollU: " , rollU
#	print "pitch angle: ", pitchAngle, " roll angle: " , rollAngle
	
        #print "Mot1: ", throttle +pitchU, " Mot2: ", throttle-pitchU

	#Start Motors
	for mot in motors:
	    mot.go()
