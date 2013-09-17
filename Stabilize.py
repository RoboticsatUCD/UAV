'''
Created on Aug 15, 2013

@author: ejracah
'''
from imu_class import IMU
from sensor_class import Sensor


delay=10
IMU.delayms=delay
MyImu=IMU(....)
MyKalman=KalmanFilter(....)
@todo: interface with throttle
    clean up
motor1=motor(....)

.
.
.
motor4-motor(....)
motors=[motor1,motor2,motor3,motor4]
RollPID=PID(.....)
PitchPID=PID(.....)
#set setpoint roll and pitch pid's to 0

#loop
#Kalman Measure
MyKalman.measure([myIMU.roll,myIMU.pitch]
rollAngle,pitchAngle=myKalman.getAngles()

#Get control inputs
rollPID.update(rollAngle)
pitchPID.update(pitchAngle)
pitchU=pitchPid.getinput/2
rollU=rollPid.getInput/2

#Set motor speeds
motor1.setSpeed(throttle+pitchU)
motor2.setSpeed(throttle+rollU)
motor3.setSpeed(throttle-pitchU)
motor4.setSpeed(throttle-rollU)

#Start Motors
for mot in motors:
    mot.go()

#Kalman Prediction
MyKalman.predict()?
time.sleep(delay)

#delay 10 ms
#repeat