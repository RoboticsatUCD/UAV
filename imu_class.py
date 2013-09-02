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

		self.prev_meas=?  #list?
	@property
	def Yaw(self):
		pass
	@property
	def Pitch(self):
		pass
	@property
	def Roll(self):
		
		#curraw=sensor.raw
		#curmeas=lowPassFilter(curraw,sensorPrevMeas)
		#prevMeas=curraw? or curmeas?
		
		self.roll_rate=((self.gyro.yRaw-self.gyro.offset)/(2**(self.gyro.numBits)-1))*self.gyro.measRange    #(raw-offset)/(total number of bits) * range of sensor= measured value of sensor
		self.gyro_roll_angle=self.rollRate*self.delayms/1000 #or maybe just plug in the actual delay time  #angular velocity times dt is angle
		
		if self.comp_filter is True: #if client activates complimentatry filter
			
			#calculate accelerometer angle
			self.accel_roll_angle=degrees(atan2(self.accel.xRaw,sqrt(self.accel.yRaw**2+self.accel.zRaw**2)))
			#use filter with accelerometer and gyro angles
			res=self.complimentaryFilter(self.gyro_roll_angle,self.accel_roll_angle)
		else:
			res=self.gyro_roll_angle
		return res
	
	
	def complimentaryFilter(self,gyro_angle,other_angle):
		return (self.gyro_weight*gyro_angle+(1.0-self.gyro_weight)*other_angle)
	
	
	def setCompFilter(self,boolean=True):
		self.comp_filter=boolean
	
	
	def getAngularRate(self,raw):
		#if its roll rate, the client will pass yraw and for pitch they will pass xraw
	
	#sets low pass filter for all the sensors
	def setLowPass(self,boolean=True):
		for sensor in sensors:
			sensor.setLowPass(boolean)

