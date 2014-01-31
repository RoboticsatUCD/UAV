#Evan Racah
#10/27/13

#Complementary Filter Class
#Will filter accelerometer and gyro angle measurements to give a filtered angle
import time
class ComplementaryFilter(object):
	def __init__(self,alpha,init_angle,time_step):
		self.alpha=alpha
		self.angle=init_angle
		self.time_step=time_step
		self.t1 = time.clock()

	def filter(self,accel_angle,gyro_rate):#should call once for each axis
		#the filter recursively calculates the angle by adding to the angle the integration 
		#of the angular velocity over the time step for the gyro and then using
		#the accelerometer angle measurement to correct for gyro drift
		#alpha*(angle+gyro*dt)+(1-alpha)*(accel)
		self.t2 = time.clock()
		self.time_step = self.t2 - self.t1
		self.t1 = self.t2
		self.angle=self.alpha*(self.angle+gyro_rate*self.time_step)+(1-self.alpha)*(accel_angle)
		return self.angle