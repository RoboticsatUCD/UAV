'''
Created on Aug 15, 2013

@author: ejracah
'''
from imu_class import IMU
from sensor_class import Sensor

"""
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
set setpoint roll and pitch pid's to 0

loop

MyKalman.measure([myIMU.roll,myIMU.pitch]
rollAngle,pitchAngle=myKalman.getAngles()
rollPID.update(rollAngle)
pitchPID.update(pitchAngle)
pitchU=pitchPid.getinput/2
rollU=rollPid.getInput/2
motor1+=pitchU
motor2+=rollU
motor3-=pitchU
motor4-=rollU
for mot in motors:
    mot.go()
MyKalman.predict()?
time.sleep(delay)
#delay 10 ms
repeat