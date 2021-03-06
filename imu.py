#Evan Racah
#8/18/2013
import time
import math
import random
from registers import *
from I2C import I2CDevice
from I2C import twosComplement as tc

from robovero.arduino import pinMode, digitalWrite, P1_0, OUTPUT
def IMUInit():
  #Enable IMU by pulling IMU_EN lowx
  pinMode(P1_0, OUTPUT)
  digitalWrite(P1_0, 0)

def IMUReset():
  #Reset IMU by pulling IMU_EN high and then lowp
  pinMode(P1_0, OUTPUT)
  digitalWrite(P1_0, 1)
  digitalWrite(P1_0, 0)


class Sensor(I2CDevice):  #I2CDevice   
	def __init__(self, address, x_low):
		I2CDevice.__init__(self, address)
		self.x_low = x_low
		self.time_of_call = time.time() #must be initially set for the first rawValue call
		self.rawValues = self.getRaw()


	def read6Reg_fake(self, x_low, registerz=6):
		"""fake read6Reg emulator that just returns random values in range for the registers"""
		max = (2**10) / 2
		return [int(random.gauss(0, max / 3)) for _ in range(registerz)]

	def rawValue(self, coordinate):
		index = xyz_map[coordinate]
		#if threshold time has passed update raw sensor values
		if (time.time() - self.time_of_call > 0.0001): #TODO DEFINE
			self.rawValues = self.getRaw() 
		return tc(self.rawValues[index], self.rawValues[index +1])
  
	def getRaw(self):
		self.time_of_call = time.time()
		#super() with no arguments can be used in python 3
		return super(Sensor,self).read6Reg(self.x_low) #
		
	def setOffsets(self,offsets=[0,0,0]):
		offsets[2] = 16384 + offsets[2]
		print offsets
		self.x_offset, self.y_offset, self.z_offset = offsets

	def calcOffsets(self, trials=10):
		xTot, yTot, zTot = [0, 0, 0]
		for trial in range(trials):
			xTot += self.rawValue('x')
			yTot += self.rawValue('y')
			zTot += self.rawValue('z')
			
		self.setOffsets([tot / trials for tot in [xTot, yTot, zTot]])



################################		
class Gyroscope(Sensor):
	def __init__(self,address=gyro_addr,full_scale=250):
		Sensor.__init__(self, address, gyro_x_low)
		self.full_scale = full_scale
		self.sensitivity = gyro_scale_map[full_scale][1]
		self.setReg()
		self.calcOffsets()
		


	def setReg(self):
		#set control registers
		super(Gyroscope, self).writeReg(gyro_ctrl_reg3, 0x08) # enable DRDY
		super(Gyroscope, self).writeReg(gyro_ctrl_reg4, 0x80) # enable block data read mode
		super(Gyroscope, self).writeReg(gyro_ctrl_reg1, gyro_scale_map[self.full_scale][0]) # normal mode, enable all axes


##################################

class Accelerometer(Sensor):
	def __init__(self,measurement_range=2,address=accel_addr):
		Sensor.__init__(self, address, accel_x_low)
		self.measurement_range = measurement_range
		self.setReg()
		self.calcOffsets()

	def setReg(self):
		#set control registers
		super(Accelerometer, self).writeReg(accel_ctrl_reg1, 0x27)
		super(Accelerometer, self).writeReg(accel_ctrl_reg4, range_map[self.measurement_range])

#########################################	

class IMU(object):
	def __init__(self):
		IMUInit();
		self.accel = Accelerometer()  #all other arguments default
		self.gyro = Gyroscope()
		
	@property
	def yaw_angle(self):
		#calculate yaw angle from compass or magnetometer
		pass

	
	@property
	def pitch_angle(self):
		self.accel_pitch_angle = math.degrees(math.atan2(self.accel.rawValue('y') - self.accel.y_offset, 
															math.sqrt( (self.accel.rawValue('x') - self.accel.x_offset) ** 2 + 
															(self.accel.rawValue('z') - self.accel.z_offset) ** 2)))
		return self.accel_pitch_angle

	#@todo clean up accel equations
	@property
	def roll_angle(self):
		self.accel_roll_angle = math.degrees(math.atan2((self.accel.rawValue('x') - 
												self.accel.x_offset), self.accel.rawValue('z') - self.accel.z_offset)) + 180
		if self.accel_roll_angle > 180:
			self.accel_roll_angle = self.accel_roll_angle - 360
		return self.accel_roll_angle

	@property
	def pitch_rate(self):
		return self.getAngularRate(self.gyro.rawValue('x'), 0)#self.gyro.x_offset)
		#angular rate of pitch motion from gyro
		

	@property
	def roll_rate(self):
		#angular roll rate from gyro
		return self.getAngularRate(self.gyro.rawValue('y'), 0)#self.gyro.y_offset)
		

	@property
	def yaw_rate(self):
		return self.getAngularRate(self.gyro.rawValue('z'), 0)#self.gyro.z_offset)

	
	def getAngularRate(self, raw, offset):
		return (raw - offset) * (self.gyro.sensitivity / 1000) #divide by 1000 because sensitivity in milli-degrees/s

if __name__=="__main__":
	imu = IMU()