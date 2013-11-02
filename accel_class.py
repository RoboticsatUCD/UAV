from sensor_class import Sensor
import time
from registers import *

#inherits sensor class
class Accelerometer(Sensor):
	def __init__(self,offsets,measurement_range=2,address=accel_addr,registers=accel_regs):
		Sensor.__init__(self,address)

		range_map={2:0x00,4:0x10,8:0x20}  #relates measurement_range value to register setup hex code for that value (2 and 4 is +/-2g and +/-4g respectively)
		
		#set location of registers where low and high bytes are for the three axes
		self.setLowHigh(registers)
		
		#digital value that corresponds 0 dps 
		self.x_offset,self.y_offset,self.z_offset=offsets
		self.numBits=bits 
		
		#sensitivity in the data sheet for accel is mdps/digit
		

		self.measurement_range=measurement_range

		#sets control registers for accel
		setReg();

	def setReg():
		#set control registers
		accel.writeReg(accel_ctrl_reg1, 0x27)
		accel.writeReg(accel_ctrl_reg4, range_map[measurement_range])

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
