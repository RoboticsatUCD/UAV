#Evan Racah
#10/27/13

#Complemetary Filter Class
#Will filter accelerometer and gyro angle measurements to give a filtered angle
class ComplemetaryFilter(object):
	def __init__(self,alpha,init_angle,time_step):
		self.alpha=alpha
		self.angle=init_angle
		self.time_step=time_step

	def filter(self,accel_angle,gyro_angle):
		#the filter recursively calculates the angle by adding the angle the integration 
		#of the angular velocity over the time step for the gyro and then using
		#the accelerometer angle measurement to correct for gyro drift

		self.angle=self.alpha*(self.angle+gyro_angle*self.time_step)+(1-self.alpha)*(accel_angle)
		return self.angle
