from sensor_class import Sensor
import time
from math import 
from

class Compass(Sensor):
	def __init__(self,offsets,sensitivity,full_scale=1.3,address=compass_addr,registers=compass_regs):
		Sensor.__init__(self,address)

		scale_map={}  #not sure what the other values are for the compass, but the default is 1.3 gauss
		
		#set location of registers where low and high bytes are for the three axes
		self.setLowHigh(registers)
		
		#digital value that corresponds 0 dps 
		self.x_offset,self.y_offset,self.z_offset=offsets
		self.numBits=bits 
		
		#sensitivity in the data sheet for compass is mdps/digit
		self.sensitivity=sensitivity

		self.full_scale=full_scale

		#sets control registers for compass
		self.setReg()

	def setReg():
		#set control registers
		compass.writeReg(compass_cra_reg, 0x18) # 75 Hz
		compass.writeReg(compass_crb_reg, 0x20) # +/- 1.3 gauss
		compass.writeReg(compass_mr_reg, 0) # continuous measurement mode

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
