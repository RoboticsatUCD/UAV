#Evan Racah
#8/18/2013
from sensor_class import Sensor
import time
from math import *

class IMU(object):
	def __init__(self,accel, compass, gyro):
		
		#copy over the three sensor objects
		self.accel=accel
		self.gyro=gyro
		self.compass=compass
		
	#@todo compass stufff
	@property
	def yaw_angle(self):
		#calculate yaw angle from compass or magnetometer
		pass

	#@todo clean up accel equations
	@property
	def pitch_angle(self):
		#calculate roll rate and then angle from roll rate
	
			self.accel_pitch_angle=degrees(atan2(self.accel.xRaw-self.accel.offset,sqrt((self.accel.yRaw-self.accel.offset)**2+(self.accel.zRaw-self.accel.offset)**2)))
			return self.accel_pitch_angle

	#@todo clean up accel equations
	@property
	def roll_angle(self):
		self.accel_roll_angle=degrees(atan2(self.accel.yRaw-self.accel.offset,sqrt((self.accel.xRaw-self.accel.offset)**2+(self.accel.zRaw-self.accel.offset)**2)))
		return self.accel_roll_angle

	@property
	def pitch_rate(self):
		return self.getAngularRate(self.gyro.xRaw)
		#angular rate of pitch motion from gyro
		pass

	@property
	def roll_rate(self):
		#angular roll rate from gyro
		return self.getAngularRate(self.gyro.yRaw)
		

	@property
	def yaw_rate(self):
		return self.getAngularRate(self.gyro.zRaw)

	

		
	#if its roll rate, the client will pass yraw and for pitch they will pass xraw
	#general formula: desired_value=(raw-offset)*sensitivity, where sensitivity is in 
	#units of what you are trying to measure (ie degrees or degrees per second) per digit as in
	#a digit in a 16 bit number

	#@todo generalize this function to take any raw,offset and scale and give back a value?
	def getAngularRate(self,raw):
		#divide by 1000 because sensitivity in the data sheet for gyro is mdps/digit, so
		#returns degrees per second (dps)
		#gyro offset is same for all axes
		return (raw-self.gyro.offset)*(gyro.sensitivity/1000) 

	
	
	

