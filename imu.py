#Evan Racah
#8/18/2013
import time
import math
import registers as rg
from I2C import I2CDevice
from I2C import twosComplement as tc

class Sensor(I2CDevice):    
	def __init__(self, address, x_low):
		I2CDevice.__init__(self, address)
		self.x_low = x_low

	def rawValue(self, index):
		#if threshold time has passed update raw sensor values
		if (t1 = time.clock()) - self.time_of_call > threshold:
			self.rawValues = self.getRaw(self.x_reg) 
		return tc(self.rawValues[index], self.rawValues[index +1])
  
	def getRaw(self,reg):
		self.time_of_call = time.clock()
		#super() with no arguments can be used in python 3
		return super(Sensor,self).read6Reg(self.x_low)
		


################################		
class Gyroscope(Sensor):
	def __init__(self,address=gyro_addr,full_scale=250):
		Sensor.__init__(self,address)
		self.full_scale = full_scale
		self.x_offset, self.y_offset, self.z_offset = offsets
		self.sensitivity = rg.gyro_scale_map[full_scale][1]
		self.setReg()

	def setReg(self):
		#set control registers
		super(Gyroscope, self).writeReg(gyro_ctrl_reg3, 0x08) # enable DRDY
		super(Gyroscope, self).writeReg(gyro_ctrl_reg4, 0x80) # enable block data read mode
		super(Gyroscope, self).writeReg(gyro_ctrl_reg1, rg.gyro_scale_map[self.full_scale][0]) # normal mode, enable all axes


##################################

class Accelerometer(Sensor):
	def __init__(self,offsets,measurement_range=2,address=accel_addr,registers=accel_regs,bits=16):
		Sensor.__init__(self,address)
		
		self.range_map = {2:0x00, 4:0x10, 8:0x20}  #relates measurement_range value to register address
		super(Accelerometer,self).setLowHigh(registers) 
		self.x_offset, self.y_offset, self.z_offset = offsets
		self.numBits = bits
		self.measurement_range = measurement_range
		self.setReg()
		self.x_Index, self.y_Index, self.z_Index = 0, 2, 4
	

	def setReg(self):
		#set control registers
		super(Accelerometer, self).writeReg(accel_ctrl_reg1, 0x27)
		super(Accelerometer, self).writeReg(accel_ctrl_reg4, self.range_map[self.measurement_range])


	def setOffset(self, offsets):
		self.x_offset, self.y_offset, self.z_offset = offsets

#########################################	

class IMU(object):
	def __init__(self):
		self.accel = Accelerometer(accel_offsets)  #all other arguments default
		self.gyro = Gyroscope(gyro_offsets)
		#self.compass=compass
		

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

	
	
	

