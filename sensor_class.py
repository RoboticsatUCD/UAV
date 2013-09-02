#Evan Racah
#8/13/2013
#Sensor Class -> Basically an abstraction of the I2CDevice class

from kalman_lib import I2CDevice, twosComplement


class Sensor(I2CDevice):    #inherits I2C device class
	def __init__(self,sensor_type,address,registers,offset,measRange,bits):
		I2CDevice.__init__(self,address)
		
		#string saying what type just in case a method acts differently based on type
		self.sensor_type=sensor_type

		#set location of registers where low and high bytes are for the three axes
		self.setLowHigh(registers)
		
		
		self.measRange=measRange # measurement range as in range of +/-g's or +/-dps
		self.offset=offset#digital value that corresponds to 0 degrees or 0 g's or 0 dps
		self.numBits=bits #bit 
	
		self.previous=[0,0,0]   #[prevx,prevy,prevz]
		self.coord_map={"x":0, "y":1,"z":2}
		
		self.low_pass=True
		self.alpha=1
	def setLowHigh(self,registers):
		#user passes in a list of tuples with [(xlow, xhigh),(ylow,yhigh),...
		#unpack tuples? (not needed?)
		self.x_reg=registers[0]
		self.y_reg=registers[1]
		self.z_reg=registers[2]

	def getRaw(self,reg,coord):
		#reads reg for x low and x high then does twos complement to get 10 bit value
		#does twos complement to get raw values
		index=self.coord_map[coord]  #index for current coordinate for any lists that have [x,y,x] ie x is 0 y is 1 z is 2
		if type is"compass":
			reg=[reg[1],reg[0]]
		
		#super() with no arguments can be used in python 3
		#returns raw value (basically combines the high byte and low byte of sensor register reading to make raw one value)
		current=twosComplement(super(Sensor,self).readReg(reg[0]), super(Sensor,self).readReg(reg[1]))
		
		if self.low_pass:
			res=self.lowPassFilter(current,self.previous[index])
		else:
			res=current
		self.previous[index]=current
		return res
		#maybe assign to variable then return just for sake of looking back at last raw value?
	@property
	def xRaw(self):
		return self.getRaw(self.x_reg,"x")
		
	@property
	def yRaw(self):
		return self.getRaw(self.y_reg,"y")
	@property
	def zRaw(self):
		return self.getRaw(self.z_reg,"z")
	
	def lowPassFilter(self,raw_meas,prev_meas):
		#low pass filter
		return raw_meas*self.alpha+(1.0-self.alpha)*self.prev_meas
	
	def setLowPass(self,boolean=True):
		self.low_pass=boolean
	def setAlpha(self,new_alpha):
		self.alpha=new_alpha

