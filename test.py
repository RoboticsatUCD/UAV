#Evan Racah
#test.py
<<<<<<< HEAD
from imu_class import IMU
from accel_class import Accelerometer

from registers import accel_offsets
#myIMU=IMU()  #instantiate IMU -> it does not take any data



accel=Accelerometer(accel_offsets)
print "hey"
=======
from robovero.extras import roboveroConfig
from imu_class import IMU
from accel_class import Accelerometer
from registers import accel_offsets
import time
#myIMU=IMU()  #instantiate IMU -> it does not take any data


roboveroConfig()
accel=Accelerometer(accel_offsets)
>>>>>>> b360148118a4be27c854783cd7757b7d41cf0666
def find_offset(sensor):
	count=0
	x_tot=0
	y_tot=0
	z_tot=0

	while(count<100):
		x=sensor.xRaw
		y=sensor.yRaw
		z=sensor.zRaw
<<<<<<< HEAD
		print "x: ",x
		print "y: ",y
		print "z: ",z
=======
#		print "x: ",x
#		print "y: ",y
#		print "z: ",z
>>>>>>> b360148118a4be27c854783cd7757b7d41cf0666
		x_tot+=x
		y_tot+=y
		z_tot+=z

		count+=1
<<<<<<< HEAD
		time.sleep(0.1)
=======
>>>>>>> b360148118a4be27c854783cd7757b7d41cf0666
	print "x avg: ",x_tot/count
	print "y avg: ",y_tot/count
	print "z avg: ",z_tot/count
find_offset(accel)
