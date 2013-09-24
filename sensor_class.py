 #Evan Racah
#8/13/2013
#Sensor Class -> Basically an abstraction of the I2CDevice class

from kalman_lib import I2CDevice, twosComplement


class Sensor(I2CDevice):    #inherits I2C device class
	def __init__(self,sensor_type,address,registers,offset,bits,sensitivity,max_voltage):
		I2CDevice.__init__(self,address)
		
		#string saying what type just in case a method acts differently based on type
		self.sensor_type=sensor_type

		#set location of registers where low and high bytes are for the three axes
		self.setLowHigh(registers)
		
		
		
		#digital value that corresponds to 0 degrees or 0 g's or 0 dps (experimentally determined)
		self.offset=offset
		self.numBits=bits 
		
		#sensitivity in the data sheet for gyro is mdps/digit for accelerometer it is mg/digit, where g is accel due to gravity
		self.sensitivity=sensitivity 
		
		#dict for ease of use in 
		self.coord_map={"x":0, "y":1,"z":2}
		
	
	def setLowHigh(self,registers):
		#user passes in a list of tuples with [(xlow, xhigh),(ylow,yhigh),...
		#unpack tuples? (not needed?)
		self.x_reg=registers[0]
		self.y_reg=registers[1]
		self.z_reg=registers[2]

  #reads reg for x low and x high then does twos complement to get full raw 16-bit value
	def getRaw(self,reg,coord):
		
		
		if type is"compass":
			reg=[reg[1],reg[0]]
		
		#super() with no arguments can be used in python 3 (
		# super basically moves up the inheritance tree until it finds first definition of function (which should be in I2CDevice class)
		#returns raw value (basically combines the high byte and low byte of sensor register reading to make raw one value)
		return twosComplement(super(Sensor,self).readReg(reg[0]), super(Sensor,self).readReg(reg[1]))
		
		

		#maybe assign to variable then return instead of just returnong for sake of looking back at last raw value?
	@property
	def xRaw(self):
		return self.getRaw(self.x_reg)
		
	@property
	def yRaw(self):
		return self.getRaw(self.y_reg)
	@property
	def zRaw(self):
		return self.getRaw(self.z_reg)

	@property
	def max_adc_value(self):
		return (2**(self.numBits)-1)

		
	
	

