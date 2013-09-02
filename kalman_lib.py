#!/usr/bin/python

from robovero.extras import Array, roboveroConfig
from robovero.lpc17xx_i2c import I2C_M_SETUP_Type, I2C_MasterTransferData, \
														I2C_TRANSFER_OPT_Type
from robovero.lpc17xx_gpio import GPIO_ReadValue
from robovero.LPC17xx import LPC_I2C0
from robovero.lpc_types import Status
import time
import math

#Axes Macros
ROLL = 0
PITCH = 1

accel_ctrl_reg1 = 0x20
accel_x_low = 0x28
accel_x_high = 0x29
accel_y_low = 0x2A
accel_y_high = 0x2B
accel_z_low = 0x2C
accel_z_high = 0x2D

compass_mr_reg = 0x02
compass_x_high = 0x03
compass_x_low = 0x04
compass_y_high = 0x05
compass_y_low = 0x06
compass_z_high = 0x07
compass_z_low = 0x08

gyro_ctrl_reg1 = 0x20
gyro_ctrl_reg2 = 0x21
gyro_ctrl_reg3 = 0x22
gyro_ctrl_reg4 = 0x23
gyro_ctrl_reg5 = 0x24
gyro_status_reg = 0x27
gyro_x_low = 0x28
gyro_x_high = 0x29
gyro_y_low = 0x2A
gyro_y_high = 0x2B
gyro_z_low = 0x2C
gyro_z_high = 0x2D
gyro_fifo_ctrl_reg = 0x2E

class I2CDevice(object):
	def __init__(self, address):
		self.config = I2C_M_SETUP_Type()
		self.tx_data = Array(2, 1)
		self.rx_data = Array(1, 1)
		self.config.sl_addr7bit = address
		self.config.tx_data = self.tx_data.ptr
		self.config.retransmissions_max = 3

	def readReg(self, register):
		self.tx_data[0] = register
		self.config.tx_length = 1
		self.config.rx_data = self.rx_data.ptr
		self.config.rx_length = 1	
		ret = I2C_MasterTransferData(LPC_I2C0, self.config.ptr,
																	I2C_TRANSFER_OPT_Type.I2C_TRANSFER_POLLING)
		if ret == Status.ERROR:
			exit("I2C Read Error")		
		return self.rx_data[0]
		
	def writeReg(self, register, value):
		self.tx_data[0] = register
		self.tx_data[1] = value
		self.config.tx_length = 2
		self.config.rx_data = 0
		self.config.rx_length = 0
		ret = I2C_MasterTransferData(LPC_I2C0, self.config.ptr,
																	I2C_TRANSFER_OPT_Type.I2C_TRANSFER_POLLING)
		if ret == Status.ERROR:
			exit("I2C Write Error")
		if self.readReg(register) != value:
			exit("I2C Verification Error")
		return None

def twosComplement(low_byte, high_byte):
	"""Unpack 16-bit twos complement representation of the result.
	"""
	return (((low_byte + (high_byte << 8)) + 2**15) % 2**16 - 2**15)

#returns current angle of particular axis
def getAngle(axis):
	#get data from accelerometers
	x_raw = twosComplement(accelerometer.readReg(accel_x_low), accelerometer.readReg(accel_x_high))
	y_raw = twosComplement(accelerometer.readReg(accel_y_low), accelerometer.readReg(accel_y_high))
	z_raw = twosComplement(accelerometer.readReg(accel_z_low), accelerometer.readReg(accel_z_high))

	#calculate angle
	if axis == ROLL: #roll
		return math.degrees(math.atan2(x_raw, math.sqrt(y_raw**2 + z_raw**2)))
	if axis == PITCH: #pitch
		return math.degrees(math.atan2(y_raw, math.sqrt(x_raw**2 + z_raw**2)))

#returns rotation around axis is deg/sec
def getRate(axis):
#	if axis == ROLL:
#		return twosComplement(gyro.readReg(gyro_y_low), gyro.readReg(gyro_y_high)) * 8.75 / 1000
	if axis == PITCH:
		return twosComplement(gyro.readReg(gyro_x_low), gyro.readReg(gyro_x_high)) * 8.75 / 1000
#	if axis == YAW:
#		return twosComplement(gyro.readReg(gyro_z_low), gyro.readReg(gyro_z_high)) * 8.75 / 1000



class Kalman:
	def __init__(self):
		self.x_angle = 0
		self.x_bias = 0
		self.P_00 = 0
		self.P_01 = 0
		self.P_10 = 0
		self.P_11 = 0

		self.y = 0
		self.S = 0
		self.K_0 = 0
		self.K_1 = 0

		self.Q_angle = 0.0
		self.Q_gyro = 0.003
		self.R_angle = 0.03

		self.t = 0

	def calculate(self):
		#check if first time through b/c t will not be set yet
		if(self.t == 0): #if (t == 0)
			self.t = time.clock()

		self.dt = time.clock() - self.t	

		self.t = time.clock()
		
		self.x_angle = self.x_angle + self.dt*(getRate(PITCH) - self.x_bias)
		self.P_00  = self.P_00 - self.dt * (self.P_10 + self.P_01) + self.Q_angle * self.dt
		self.P_01 = self.P_01 - self.dt * self.P_11
		self.P_10 = self.P_10 - self.dt * self.P_11
		self.P_11 = self.P_11 + self.Q_gyro * self.dt

		self.error = getAngle(PITCH) - self.x_angle
		self.S = self.P_00 + self.R_angle
		self.K_0 = self.P_00 / self.S
		self.K_1 = self.P_10 / self.S

		self.x_angle = self.x_angle + self.K_0 * self.error
		self.x_bias = self.x_bias + self.K_1 * self.error 
		self.P_00 = self.P_00 - self.K_0 * self.P_00
		self.P_01 = self.P_01 - self.K_0 * self.P_01
		self.P_10 = self.P_10 - self.K_1 * self.P_10
		self.P_11 = self.P_11 - self.K_1 * self.P_11

		return self.x_angle

class PID:
	def __init__(self, p, i, d):
		self.Kp = p
		self.Ki = i
		self.Kd = d

		self.total_error = 0
		self.prev_error= 0 #derivator

		self.max_total_error = 1000
		self.min_total_error = -1000

		self.setpoint= 0
		self.error = 0

	def update(self, current):
		self.error = self.setpoint - current

		self.P = self.Kp * self.error
		self.D = self.Kd * (self.error - self.prev_error)

		self.prev_error = self.error

		self.total_error = self.total_error + self.error

		if self.total_error > self.max_total_error:
			print 'Reached max error!'
			self.total_error = self.max_total_error
		elif self.total_error < self.min_total_error:
			print 'Reached min error!'
			self.total_error = self.min_total_error

		self.I =  self.Ki * self.total_error

		PID = self.P + self.I + self.D

		return PID

	def setPoint(self, point):
		self.setpoint = point
		self.total_error = 0
		self.error = 0

"""
if __name__ == '__main__':
	# Initialize pin select registers
	roboveroConfig()

	# configure accelerometer
	accelerometer = I2CDevice(0x18)
	accelerometer.writeReg(accel_ctrl_reg1, 0x27)

	# configure compass
	#compass = I2CDevice(0x1E)
	#compass.writeReg(compass_mr_reg, 0)	# continuous measurement mode

	# configure the gyro
	# see L3G4200D Application Note for initialization procedure
	gyro = I2CDevice(0x68)
	#gyro.writeReg(gyro_ctrl_reg2, 0x20) # test setting
	gyro.writeReg(gyro_ctrl_reg3, 0x08) # enable DRDY
	gyro.writeReg(gyro_ctrl_reg4, 0x00) # enable block data read mode
	gyro.writeReg(gyro_ctrl_reg1, 0x0A)	# normal mode, enable x-axis, 0x0F for x,y,z 

	#create Kalman filter
	imu = Kalman()

	#create PID
	control = PID(2.0, 1.0, 1.0)

	while True:
		angle = imu.calculate()
		pwm = control.update(angle)

		print 'Angle:', angle,
		print 'PWM:', pwm
"""
