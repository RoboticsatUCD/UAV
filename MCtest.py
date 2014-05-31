"""Simple control of of one brushed DC motor using a MOSFET using the 
MC0A0 pin of the RoboVero
"""

from robovero.lpc17xx_mcpwm import MCPWM_Init, MCPWM_CHANNEL_CFG_Type, \
                      MCPWM_ConfigChannel, MCPWM_DCMode, MCPWM_ACMode, \
                      MCPWM_Start, MCPWM_WriteToShadow, MCPWM_Stop,    \
                      MCPWM_CHANNEL_EDGE_MODE, MCPWM_CHANNEL_PASSIVE_HI, MCPWM_CHANNEL_PASSIVE_LO
from robovero.extras import roboveroConfig
from robovero.LPC17xx import LPC_MCPWM
from robovero.lpc_types import FunctionalState
from time import sleep

__author__ =      "Danny Chan"
__email__ =       "danny@gumstix.com"
__copyright__ =   "Copyright 2012, Gumstix Inc."
__license__ =     "BSD 2-Clause"

periodValue = 600000
ENABLE = FunctionalState.ENABLE
DISABLE = FunctionalState.DISABLE

def getMotorSpeed():
  """Get an angle from the user and calculate new duty cycle.
  """
  user_speed = raw_input("New Speed (%): ")
  try:
		speed = int(user_speed)
		if speed < 0 or speed > 100:
			raise InputError
  except:
    print "enter an speed between 0% and 100%"
    return None
  match_value = speed*300 + 30000
  return match_value
  
roboveroConfig()

MCPWM_Init(LPC_MCPWM)

channelsetup = MCPWM_CHANNEL_CFG_Type()
  
channelsetup.channelType = MCPWM_CHANNEL_EDGE_MODE
channelsetup.channelPolarity = MCPWM_CHANNEL_PASSIVE_HI
channelsetup.channelDeadtimeEnable = DISABLE
channelsetup.channelDeadtimeValue = 0
channelsetup.channelUpdateEnable = ENABLE
channelsetup.channelTimercounterValue = 0
channelsetup.channelPeriodValue = periodValue
channelsetup.channelPulsewidthValue = 0

for i in xrange(0,6):
	MCPWM_ConfigChannel(LPC_MCPWM, i, channelsetup.ptr)

# Disable DC Mode
MCPWM_DCMode(LPC_MCPWM, DISABLE, DISABLE, (0))

# Disable AC Mode
MCPWM_ACMode(LPC_MCPWM, DISABLE)

MCPWM_Start(LPC_MCPWM, ENABLE, ENABLE, ENABLE)

try:
  while True:
	chan = int(raw_input("Pick a channel: "))
	channelsetup.channelPulsewidthValue = getMotorSpeed()
	MCPWM_WriteToShadow(LPC_MCPWM, chan, channelsetup.ptr)
except:
  MCPWM_Stop(LPC_MCPWM, ENABLE, DISABLE, DISABLE)
  print "you broke it"
