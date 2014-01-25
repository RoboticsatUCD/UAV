# accessing proper header/implementation files for motor stuff
from robovero.LPC17xx import LPC_PWM1
from robovero.lpc17xx_pwm import PWM_TC_MODE_OPT, \
          PWM_MATCH_UPDATE_OPT, PWM_MATCHCFG_Type, \
          PWM_MatchUpdate, PWM_ConfigMatch, PWM_ChannelCmd, \
          PWM_ResetCounter, PWM_CounterCmd, PWM_Cmd
from robovero.extras import roboveroConfig, initMatch
from robovero.lpc_types import FunctionalState

from robovero.arduino import analogWrite, PWM1

from custom_servo import initPulse, initPeriod, initPWM


#access class for getting ps2 readings
from ps2_read import *
ZERO=130
MAX=255


"""bytes=[ZERO,ZERO,ZERO,ZERO] #set speeds
shapes=[1,0,1,0]
stick=200 
"""

"""
UAV motor speed schematic, with each number representing index of speeds list
		0
		|
	3-------1
		|
		2
Also 0->triangle, 1->circle, 2->X, 3-> square
"""
#enter in speed as percentage and the correct pulse width for the motor is returned
def byte_to_pulse(byte):
	byte=min(max(byte,ZERO),MAX) 			#makes sure speed between ZERO and MAX
	pulse=8*byte-40 						#scales bit value to pulse: ZERO (130) leads to 1000 ms pulse, MAX (255) leads to a 2000 ms pulse
	return pulse


		

roboveroConfig()      #configures robovero (not sure exactly what this does)


#sets up pwm with the period, the pulse width and then gives the motor controller a high, a low and a mid signal and then low one again, so it begins stopped
initPWM()             


#This loop gets the data from Ps2 then pulses motors accordingly
Ps2=Ps2Control() 
while (1):
	Ps2.refresh()
	
	"""Get data from ps2 controller"""
	
	stick=Ps2.read_sticks() 
	shapes=Ps2.read_shape()
	
	
	
	"""If none of the boolean values in shapes array are 1 (ie no shapes pressed)"""
	if not any(shapes): 
		"""set all bits to bit value"""
		bytes=[stick]*4
	
	else:        #at least one button is pushed
	
		i=0
		while i<4:
			"""If shape value (shapes[i]) is 1 (pressed) then byte set to stick value"""
			if shapes[i]:
				bytes[i]=stick
			i=i+1
	
	"""Pulse motors assuming:
		Port 1: bytes[0], shapes[0], triangle
		Port 2: bytes[1], shapes[1], circle
		"""

	while i<4:
		initPulse(i+1,byte_to_pulse(bytes[i])
		i=i+1
	
	
	
	
	
	"""
	
	TEST:
	Must comment out any functions from other files first if testing without being rigged
	up to robovero and ps2 and use counter for while loop
	
	print "Bytes:", bytes
	print "Pulses", byte_to_pulse(bytes[0])
	stick=stick-5
	print "Stick:", stick
	if j%2==0:
		shapes=[1,0,1,0]
	else:
		shapes=[0,0,0,0]
	print "Shapes:", shapes
	""""
	j=j+1
	





