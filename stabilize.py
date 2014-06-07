"""
Created on Aug 15, 2013

@author: Evan Racah
"""


from imu import IMU
from robovero.extras import roboveroConfig
import time
from ComplementaryFilter import ComplementaryFilter
from motor2 import Motor
from PID import PIDControl
import signal
import sys
import thread

roboveroConfig()

#Initialize motors

m1 = Motor(2, True)
m2 = Motor(1, True)
m3 = Motor(1, False)
m4 = Motor(6, False)

m4.initAll()

# Initialize IMU
imu = IMU()
cfRoll = ComplementaryFilter(0.9, 0)
cfPitch = ComplementaryFilter(0.9, 0)

pitchPID = PIDControl(0, [0.168, 0.654 ,0.008])
rollPID = PIDControl(0, [0.5, 0.5 ,0])

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    for m in m4.motors:
        m.setSpeed(0)
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
	
	rollAngle = cfRoll.filter(imu.roll_angle, imu.roll_rate)
	pitchAngle = cfPitch.filter(imu.pitch_angle, imu.pitch_rate)
	
	pitchU = (pitchPID.update(pitchAngle))
	rollU = (rollPID.update(rollAngle))
	
	throttle = 500
	#Set motor speeds
	m1.setSpeed(throttle + rollU)
	m2.setSpeed(throttle - rollU)
	#motor3.setSpeed(throttle - pitchU)
	#motor4.setSpeed(throttle - rollU)

	print "pitchU: ", pitchU, " rollU: " , rollU
	print "pitch angle: ", pitchAngle, " roll angle: " , rollAngle
	
    #print "Mot1: ", throttle +pitchU, " Mot2: ", throttle-pitchU
