#Evan Racah
#8/18/2013
import time, math
from registers import accel_offsets, gyro_offsets
from I2C_Class import I2CDevice

class Sensor(I2CDevice):    
	def __init__(self,address):
		I2CDevice.__init__(self,address)
		
		#self.raw_values=super(Sensor,self).read6Reg(accel_x_low)
		
	def setLowHigh(self,registers):
		#unpacks tuples with register addresses
		self.x_reg, self.y_reg, self.z_reg = registers[0], registers[1], registers[2]

  
	def getRaw(self,reg):
		#super() with no arguments can be used in python 3 (
		# super basically moves up the inheritance tree until it finds first definition of function (which should be in I2CDevice class)
		#returns raw value (basically combines the high byte and low byte of sensor register reading to make raw one value)
		
		return twosComplement(super(Sensor, self).readReg(reg[0]), super(Sensor, self).readReg(reg[1]))
		#if flag==1:
			#self.raw_values=super(Sensor,self).read6Reg(accel_x_low)

		#return twosComplement(self.raw_values[index], self.raw_values[index+1])


################################		
class Gyroscope(Sensor):
	def __init__(self,offsets,full_scale=250,address=gyro_addr,registers=gyro_regs,bits=16):
		Sensor.__init__(self,address)
		self.scale_map = {250:0x0F,500:0x1F,2000:0x2F}  #relates full_scale value to register address
		self.sensitivity_map = {250:8.75,500:17.5,2000:70}  #maps measurement range to sensitivity in milli-degrees/sec
		self.setLowHigh(registers)
		self.x_offset, self.y_offset, self.z_offset = offsets
		self.numBits = bits 
		self.full_scale = full_scale
		self.sensitivity = self.sensitivity_map[self.full_scale]
		self.setReg()

	def setReg(self):
		#set control registers
		super(Gyroscope, self).writeReg(gyro_ctrl_reg3, 0x08) # enable DRDY
		super(Gyroscope, self).writeReg(gyro_ctrl_reg4, 0x80) # enable block data read mode
		super(Gyroscope, self).writeReg(gyro_ctrl_reg1, self.scale_map[self.full_scale]) # normal mode, enable all axes, whatever full-scale use selects (250,500 or 2000dps)

	@property
	def xRaw(self):
		return super(Gyroscope, self).getRaw(self.x_reg) #super(base,inherited) looks up the inheritance tree until it finds the function
		
	@property
	def yRaw(self):
		return super(Gyroscope, self).getRaw(self.y_reg)
	@property
	def zRaw(self):
		return super(Gyroscope, self).getRaw(self.z_reg)

	@property
	def max_adc_value(self):
		return (2**(self.numBits)-1)


#########################################	

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

	@property
	def xRaw(self):
		return super(Accelerometer, self).getRaw(self.x_reg) #super(base,inherited) looks up the inheritance tree until it finds the function
		
	@property
	def yRaw(self):
		return super(Accelerometer, self).getRaw(self.y_reg)
	@property
	def zRaw(self):
		return super(Accelerometer, self).getRaw(self.z_reg)

	@property
	def max_adc_value(self):
		return ( 2** (self.numBits) - 1)

	def setOffset(self, offsets):
		self.x_offset, self.y_offset, self.z_offset = offsets

#########################################	

class IMU(object):
	def __init__(self):
		self.accel = Accelerometer(accel_offsets)  #all other arguments default
		self.gyro = Gyroscope(gyro_offsets)
		#self.compass=compass
		
	#@todo compass stufff
	@property
	def yaw_angle(self):
		#calculate yaw angle from compass or magnetometer
		pass

	#@todo clean up accel equations
	@property
	def pitch_angle(self):
		self.accel_pitch_angle = degrees(atan2(self.accel.yRaw - self.accel.y_offset, 
															sqrt( (self.accel.xRaw - self.accel.x_offset) ** 2 + 
															(self.accel.zRaw - self.accel.z_offset) ** 2)))
		return self.accel_pitch_angle

	#@todo clean up accel equations
	@property
	def roll_angle(self):
		self.accel_roll_angle = degrees(atan2((self.accel.xRaw - self.accel.x_offset), self.accel.zRaw - self.accel.z_offset)) + 180
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

	
	
	

