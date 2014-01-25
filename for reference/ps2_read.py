from struct import unpack

class Ps2Control:
	f = open("/dev/usbmon1","rb")
	info = 0
	p2 = 0
	p2shoulder = 0
	p2shape = 0
	def __init__(self):
		self.info = unpack('BBBBBBBBBBBBBBBB', self.f.read(16))
		if(self.info[0] == 2):
			self.p2 = 0
		else:
			self.p2 = 8
		self.p2shoulder = self.p2 + 6
		self.p2shape = self.p2 + 5
	def refresh(self):
		self.info = unpack('BBBBBBBBBBBBBBBB', self.f.read(16))
	def read_sticks(self):
		return self.info[self.p2+1:self.p2+5]
	def read_shoulder(self):
		"""returns boolean values indicating whether buttons are pressed"""
		"""[L2, R2, L1, R1, select, start, L3, R3]"""
		byte = self.info[self.p2shoulder]
		return [(byte & 1) != 0, (byte & 2) !=0, (byte & 4)!=0, (byte & 8)!=0, (byte & 16)!=0, (byte & 32)!=0, (byte & 64)!=0, (byte & 128)!=0]
	def read_shape(self):
		"""[triangle, circle, X, square]"""
		byte = self.info[self.p2shape]
		return [(byte & 16) != 0, (byte & 32) != 0, (byte & 64) != 0, (byte & 128) != 0]
	def read_Dpad(self):
		"""[Up, Right, Down, Left]"""
		byte = self.info[self.p2shape] & 15
		return [(byte == 0 or byte == 1 or byte == 7), (byte == 1 or byte == 2 or byte == 3), (byte == 3 or byte == 4 or byte == 5), (byte == 5 or byte == 6 or byte == 7)];



control = Ps2Control()
while(1):
	print control.refresh()
	print control.read_sticks()
	print control.read_shoulder()
	print control.read_shape()
	print control.read_Dpad()




