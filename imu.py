#Evan Racah
#8/18/2013
import time
import math
from registers import *
from I2C import I2CDevice
from I2C import twosComplement as tc



class Sensor(I2CDevice):    
	def __init__(self, address, x_low):
		I2CDevice.__init__(self, address)
		self.x_low = x_low

	def read6Reg_fake(self, x_low, registerz=6):
	"fake read6Reg emulator that just returns random values in range for the registers"
		max = (2**16) / 2
		return [randint(-max,max) for _ in range(registerz)]

	def rawValue(self, coordinate):
		index = xyz_map[coordinate]
		#if threshold time has passed update raw sensor values
		if (t1 = time.clock()) - self.time_of_call > threshold:
			self.rawValues = self.getRaw(self.x_reg) 
		return tc(self.rawValues[index], self.rawValues[index +1])
  
	def getRaw(self,reg):
		self.time_of_call = time.clock()
		#super() with no arguments can be used in python 3
		return super(Sensor,self).read6Reg_fake(self.x_low)
		
	def setOffsets(self,offsets=[0,0,0]):
		self.x_offset, self.y_offset, self.z_offset = offsets

	def calcOffsets(self, trials=10):
		xTot, yTot, zTot = 0
		for trial in range(trials):
			xTot += self.rawValue('x')
			yTot += self.rawValue('y')
			zTot += self.rawValue('z')
			time.sleep(1)
		self.setOffsets([tot / trials for tot in [xTot, yTot, zTot]])



################################		
class Gyroscope(Sensor):
	def __init__(self,address=gyro_addr,full_scale=250):
		Sensor.__init__(self,address)
		self.full_scale = full_scale
		self.sensitivity = gyro_scale_map[self.full_scale][1]
		self.setReg()
		super(Gyroscope, self).Offsets()

	def setReg(self):
		#set control registers
		super(Gyroscope, self).writeReg(gyro_ctrl_reg3, 0x08) # enable DRDY
		super(Gyroscope, self).writeReg(gyro_ctrl_reg4, 0x80) # enable block data read mode
		super(Gyroscope, self).writeReg(gyro_ctrl_reg1, gyro_scale_map[self.full_scale][0]) # normal mode, enable all axes


##################################

class Accelerometer(Sensor):
	def __init__(self, address=accel_addr, measurement_range=2):
		Sensor.__init__(self,address)
		self.measurement_range = measurement_range
		self.setReg()
		super(Accelerometer, self).calcOffsets()
	
	
	def setReg(self):
		#set control registers
		super(Accelerometer, self).writeReg(accel_ctrl_reg1, 0x27)
		super(Accelerometer, self).writeReg(accel_ctrl_reg4, self.range_map[self.measurement_range])


#########################################	

class IMU(object):
	def __init__(self):
		#these two constructors should be called when the uav is level in order to calculate offset
		self.accel = Accelerometer()  #all other arguments default
		self.gyro = Gyroscope()
	
		
		
	@property
	def yaw_angle(self):
		#calculate yaw angle from compass or magnetometer
		pass

	
	@property
	def pitch_angle(self):
		self.accel_pitch_angle = degrees(atan2(self.accel.yRaw - self.accel.y_offset, 
															sqrt( (self.accel.xRaw - self.accel.x_offset) ** 2 + 
															(self.accel.zRaw - self.accel.z_offset) ** 2)))
		return self.accel_pitch_angle

	#@todo clean up accel equations
	@property
	def roll_angle(self):
		self.accel_roll_angle = degrees(atan2((self.accel.xRaw - 
												self.accel.x_offset), self.accel.zRaw - self.accel.z_offset)) + 180
		if self.accel_roll_angle > 180:
			self.accel_roll_angle = self.accel_roll_angle - 360
		return self.accel_roll_angle

	@property
	def pitch_rate(self):
		return self.getAngularRate(self.gyro.xRaw, self.gyro.x_offset)
		#angular rate of pitch motion from gyro
		

	@property
	def roll_rate(self):
		#angular roll rate from gyro
		return self.getAngularRate(self.gyro.yRaw, self.gyro.y_offset)
		

	@property
	def yaw_rate(self):
		return self.getAngularRate(self.gyro.zRaw, self.gyro.z_offset)

	
	def getAngularRate(self, raw, offset):
		return (raw - offset) * (self.gyro.sensitivity / 1000) #divide by 1000 because sensitivity in milli-degrees/s

	
	
	

