from sensor_class import Sensor
import time
from registers import *

class Gyroscope(Sensor):
	def __init__(self,offsets,full_scale=250,address=gyro_addr,registers=gyro_regs,bits=16):
		Sensor.__init__(self,address)

		self.scale_map={250:0x0F,500:0x1F,2000:0x2F}  #relates full_scale value to register setup hex code for that value
		self.sensitivity_map={250:8.75,500:17.5,2000:70}  #maps measurement range to sensitivity in milli-degrees/sec
		
		#set location of registers where low and high bytes are for the three axes
		self.setLowHigh(registers)
		
		#digital value that corresponds 0 dps 
		self.x_offset,self.y_offset,self.z_offset=offsets
		self.numBits=bits 
		

		self.full_scale=full_scale
		#sensitivity in the data sheet for gyro is mdps/digit
		self.sensitivity=self.sensitivity_map[self.full_scale]

		

		#sets control registers for gyro
		self.setReg()

	def setReg(self):
		#set control registers
		
		super(Gyroscope,self).writeReg(gyro_ctrl_reg3, 0x08) # enable DRDY
		super(Gyroscope,self).writeReg(gyro_ctrl_reg4, 0x80) # enable block data read mode
		super(Gyroscope,self).writeReg(gyro_ctrl_reg1, self.scale_map[self.full_scale]) # normal mode, enable all axes, whatever full-scale use selects (250,500 or 2000dps)

	@property
	def xRaw(self):
		return super(Gyroscope,self).getRaw(self.x_reg) #super(base,inherited) looks up the inheritance tree until it finds the function
		
	@property
	def yRaw(self):
		return super(Gyroscope,self).getRaw(self.y_reg)
	@property
	def zRaw(self):
		return super(Gyroscope,self).getRaw(self.z_reg)

	@property
	def max_adc_value(self):
		return (2**(self.numBits)-1)

