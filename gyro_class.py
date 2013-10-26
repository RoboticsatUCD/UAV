from sensor_class import Sensor
import time
from math import 
from registers import *

class Gyroscope(Sensor):
	def __init__(self,offsets,sensitivity,full_scale=250,address=gyro_addr,registers=gyro_regs):
		Sensor.__init__(self,address)

		scale_map={250:0x0F,500:0x1F,2000:0x2F}  #relates full_scale value to register setup hex code for that value
		
		#set location of registers where low and high bytes are for the three axes
		self.setLowHigh(registers)
		
		#digital value that corresponds 0 dps 
		self.x_offset,self.y_offset,self.z_offset=offsets
		self.numBits=bits 
		
		#sensitivity in the data sheet for gyro is mdps/digit
		self.sensitivity=sensitivity

		self.full_scale=full_scale

		#sets control registers for gyro
		setReg();

	def setReg():
		#set control registers
		gyro.writeReg(gyro_ctrl_reg3, 0x08) # enable DRDY
		gyro.writeReg(gyro_ctrl_reg4, 0x80) # enable block data read mode
		gyro.writeReg(gyro_ctrl_reg1, scale_map[full_scale]) # normal mode, enable all axes, whatever full-scale use selects (250,500 or 2000dps)

	@property
	def xRaw(self):
		return super(Sensor,self).getRaw(self.x_reg) #super(base,inherited) looks up the inheritance tree until it finds the function
		
	@property
	def yRaw(self):
		return super(Sensor,self).getRaw(self.y_reg)
	@property
	def zRaw(self):
		return super(Sensor,self).getRaw(self.z_reg)

	@property
	def max_adc_value(self):
		return (2**(self.numBits)-1)

