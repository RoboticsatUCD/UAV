 #Evan Racah
#8/13/2013

#Sensor Class -> Basically an abstraction of the I2CDevice class

from I2C_Class import * #gets the I2C_Class and twoscomplement function
from registers import *



class Sensor(I2CDevice):    #inherits I2C device class
	def __init__(self,address):
		I2CDevice.__init__(self,address)
		
	
		
	def setLowHigh(self,registers):
		#user passes in a list of tuples with [(xlow, xhigh),(ylow,yhigh),...
		#unpack tuples? (not needed?)
		self.x_reg=registers[0]
		self.y_reg=registers[1]
		self.z_reg=registers[2]

  #reads reg for x low and x high then does twos complement to get full raw 16-bit value
	def getRaw(self,reg):
		

		#super() with no arguments can be used in python 3 (
		# super basically moves up the inheritance tree until it finds first definition of function (which should be in I2CDevice class)
		#returns raw value (basically combines the high byte and low byte of sensor register reading to make raw one value)
		return twosComplement(super(Sensor,self).readReg(reg[0]), super(Sensor,self).readReg(reg[1]))
		
		


	
		
	
	

