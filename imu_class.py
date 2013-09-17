#Evan Racah
#8/18/2013
from sensor_class import Sensor
import time
from math import *

class IMU(object):
	def __init__(self,registers,addresses):
		#registers is a list of 3 lists for the registers for acc, gyro and compass
		#addresses gives a tuple of accelerometer address,gyro and compass
		
		#unpack addresses
		self.accel_ad,self.gyro_ad,self.comp_ad=addresses

		#unpack registers
		self.accel_reg,self.gyro_reg,self.comp_reg=addresses
		
		#instantiate the three sensor objects
		self.accel=Sensor("accelerometer",self.accel_ad,self.accel_reg)
		self.gyro=Sensor("gyroscope",self.gyro_ad,self.gyro_reg)
		self.compass=Sensor("compass",self.compass_ad,self.compass_reg)
		
		sensors=[self.accel,self.gyro,self.compass];
		
		self.t=0
		self.gyroWeight=0.9
		self.alpha=0.5
		self.delayms=10
		self.comp_filter=False

		#initialize to zero means we assume UAV horisontal at start
		#we could make this equal to an initial acceleromter measurement
		self.gyro_roll_angle=0  
	@property
	def yaw_angle(self):
		#calculate yaw angle from compass or magnetometer
		pass

	@property
	def pitch_angle(self):
		#calculate roll rate and then angle from roll rate
	
			self.accel_pitch_angle=degrees(atan2(self.accel.xRaw-self.accel.zero,sqrt((self.accel.yRaw-self.accel.zero)**2+(self.accel.zRaw-self.accel.zero)**2)))
			return self.accel_pitch_angle
	
	@property
	def roll_angle(self):
		self.accel_roll_angle=degrees(atan2(self.accel.yRaw-self.accel.zero,sqrt((self.accel.xRaw-self.accel.zero)**2+(self.accel.zRaw-self.accel.zero)**2)))
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
		#yaw rate from gyro
		pass

	def complimentaryFilter(self,gyro_angle,other_angle):
		return (self.gyro_weight*gyro_angle+(1.0-self.gyro_weight)*other_angle)
	
	
	def setCompFilter(self,boolean=True):
		self.comp_filter=boolean
		
	
	def getAngularRate(self,raw):
		#if its roll rate, the client will pass yraw and for pitch they will pass xraw
		den=(gyro.sensitivity/gyro.maxV)*(2**(self.gyro.numBits)-1)  #units here are bits/degrees/second
		return (raw-self.gyro.zero)/den 
	#sets low pass filter for all the sensors
	def setLowPass(self,boolean=True):
		for sensor in sensors:
			sensor.setLowPass(boolean)
	

