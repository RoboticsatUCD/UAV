#!/usr/bin/python

from robovero.extras import Array, roboveroConfig
from robovero.lpc17xx_i2c import I2C_M_SETUP_Type, I2C_MasterTransferData, \
														I2C_TRANSFER_OPT_Type
from robovero.lpc17xx_gpio import GPIO_ReadValue
from robovero.LPC17xx import LPC_I2C0
from robovero.lpc_types import Status
import time
import math



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