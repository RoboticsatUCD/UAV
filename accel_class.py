from sensor_class import *
import time
from registers import *

#inherits sensor class
class Accelerometer(Sensor):
	def __init__(self,offsets,measurement_range=2,address=accel_addr,registers=accel_regs,bits=16):
		Sensor.__init__(self,address)
		self.range_map={2:0x00,4:0x10,8:0x20}  #relates measurement_range value to register setup hex code for that value (2 and 4 is +/-2g and +/-4g respectively)
		
		#set location of registers where low and high bytes are for the three axes
		super(Accelerometer,self).setLowHigh(registers)
		
		#digital value that corresponds 0 dps 
		self.x_offset,self.y_offset,self.z_offset=offsets
		self.numBits = bits
		
		#sensitivity in the data sheet for accel is mdps/digit
		

		self.measurement_range = measurement_range

		#sets control registers for accel
		
		self.setReg()

		self.x_Index = 0
		self.y_Index = 2
		self.z_Index = 4

	def setReg(self):
		#set control registers
	
		super(Accelerometer,self).writeReg(accel_ctrl_reg1, 0x27)
		super(Accelerometer,self).writeReg(accel_ctrl_reg4, self.range_map[self.measurement_range])
	@property
	def xRaw(self):
		return super(Accelerometer,self).getRaw(self.x_reg) #super(base,inherited) looks up the inheritance tree until it finds the function
		
	@property
	def yRaw(self):
		return super(Accelerometer,self).getRaw(self.y_reg)
	@property
	def zRaw(self):
		return super(Accelerometer,self).getRaw(self.z_reg)

	@property
	def max_adc_value(self):
		return (2**(self.numBits)-1)

	def setOffset(self,offsets):
		self.x_offset,self.y_offset,self.z_offset=offsets
