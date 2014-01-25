"""Set position of servo 1 (PWM1) to an angle provided by the user.

You must have an RC servo connected to PWM1 for this example. Otherwise, you
can observe the control signal with an oscilloscope or logic analyzer.
"""
import time
from robovero.LPC17xx import LPC_PWM1
from robovero.lpc17xx_pwm import PWM_TC_MODE_OPT, \
					PWM_MATCH_UPDATE_OPT, PWM_MATCHCFG_Type, \
					PWM_MatchUpdate, PWM_ConfigMatch, PWM_ChannelCmd, \
					PWM_ResetCounter, PWM_CounterCmd, PWM_Cmd
from robovero.extras import roboveroConfig, initMatch
from robovero.lpc_types import FunctionalState

from robovero.arduino import analogWrite, PWM1, PWM2, PWM3, PWM4

__author__ =			"Neil MacMunn"
__email__ =				"neil@gumstix.com"
__copyright__ = 	"Copyright 2010, Gumstix Inc"
__license__ = 		"BSD 2-Clause"
__version__ =			"0.1"


def getSpeed():
	"""Get an angle from the user and calculate new duty cycle.
	"""
	user_speed = raw_input("New speed ")
	try:
		angle = int(user_speed)
		if angle < 0 or angle > 100:
			raise InputError
	except:
		print "enter a speed between 0 and 100"
		return None
	return 10.0*angle

def initPulse(channel, pulse_width):
	initMatch(channel, pulse_width)
	
def initPeriod(period):
	initMatch(0, period)

def initPWM():
	"""Set up PWM to output a 1.5ms pulse at 50Hz.
	"""

	# Set the period to 20000us = 20ms = 50Hz
	initPeriod(20000)

	# Set the pulse width to 1.5ms
	initPulse(1, 1500)
	initPulse(2, 1500)
	initPulse(3, 1500)
	initPulse(4, 1500)
	
	
	PWM_ChannelCmd(LPC_PWM1, 1, FunctionalState.ENABLE)
	PWM_ResetCounter(LPC_PWM1)
	PWM_CounterCmd(LPC_PWM1, FunctionalState.ENABLE)
	PWM_Cmd(LPC_PWM1, FunctionalState.ENABLE)

	PWM_ChannelCmd(LPC_PWM1, 2, FunctionalState.ENABLE)
	PWM_ResetCounter(LPC_PWM1)
	PWM_CounterCmd(LPC_PWM1, FunctionalState.ENABLE)
	PWM_Cmd(LPC_PWM1, FunctionalState.ENABLE)

	PWM_ChannelCmd(LPC_PWM1, 3, FunctionalState.ENABLE)
	PWM_ResetCounter(LPC_PWM1)
	PWM_CounterCmd(LPC_PWM1, FunctionalState.ENABLE)
	PWM_Cmd(LPC_PWM1, FunctionalState.ENABLE)

	PWM_ChannelCmd(LPC_PWM1, 4, FunctionalState.ENABLE)
	PWM_ResetCounter(LPC_PWM1)
	PWM_CounterCmd(LPC_PWM1, FunctionalState.ENABLE)
	PWM_Cmd(LPC_PWM1, FunctionalState.ENABLE)
	initPulse(1, 2000)
	initPulse(1, 1000)
	initPulse(1, 1500)
	#time.sleep(0.5)
	initPulse(1, 1000)

	initPulse(2, 2000)
	#time.sleep(0.5)
	initPulse(2, 1000)
	#time.sleep(0.5)
	initPulse(2, 1500)
	#time.sleep(0.5)
	initPulse(2, 1000)

	initPulse(3, 2000)
	#time.sleep(0.5)
	initPulse(3, 1000)
	#time.sleep(0.5)
	initPulse(3, 1500)
	#time.sleep(0.5)
	initPulse(3, 1000)

	initPulse(4, 2000)
	#time.sleep(0.5)
	initPulse(4, 1000)
	#time.sleep(0.5)
	initPulse(4, 1500)
	#time.sleep(0.5)
	initPulse(4, 1000)


if __name__ == "__main__":
 # Entry Point
  roboveroConfig()
  initPWM()

  while True:
    pulse = getSpeed()
    out = 1000 + pulse
    initPulse(5, out)
    print 5
    initPulse(2, out)
    print 2
    initPulse(3, out)
    print 3
    initPulse(4, out)
    print 4
		


