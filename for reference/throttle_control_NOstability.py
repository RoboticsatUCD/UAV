"""CUSTOM SERVO LIBRARY VERSION. NO EXECUTABLE STATEMENTS """
"""Set position of servo 1 (PWM1) to an angle provided by the user.

You must have an RC servo connected to PWM1 for this example. Otherwise, you
can observe the control signal with an oscilloscope or logic analyzer.
"""
import time, math
from robovero.LPC17xx import LPC_PWM1
from robovero.lpc17xx_pwm import PWM_TC_MODE_OPT, \
                    PWM_MATCH_UPDATE_OPT, PWM_MATCHCFG_Type, \
                    PWM_MatchUpdate, PWM_ConfigMatch, PWM_ChannelCmd, \
                    PWM_ResetCounter, PWM_CounterCmd, PWM_Cmd
from robovero.extras import roboveroConfig, initMatch
from robovero.lpc_types import FunctionalState

from robovero.arduino import analogWrite, PWM1

from network_controller import network_controller

__author__ =            "Neil MacMunn"
__email__ =             "neil@gumstix.com"
__copyright__ =     "Copyright 2010, Gumstix Inc"
__license__ =       "BSD 2-Clause"
__version__ =           "0.1"

def initPulse(channel, pulse_width):
    initMatch(channel, pulse_width)
    
def initPeriod(period):
    initMatch(0, period)

def initPWM():
    #Set up PWM to output a 1.0ms pulse at 50Hz.
    

    # Set the period to 20000us = 20ms = 50Hz
    initPeriod(20000)

    # Set the pulse width to 1.0ms
    initPulse(1, 1000)
    initPulse(2, 1000)
    initPulse(5, 1000)
    initPulse(4, 1000)
    
    PWM_ChannelCmd(LPC_PWM1, 1, FunctionalState.ENABLE)
    PWM_ChannelCmd(LPC_PWM1, 2, FunctionalState.ENABLE)
    PWM_ChannelCmd(LPC_PWM1, 5, FunctionalState.ENABLE)
    PWM_ChannelCmd(LPC_PWM1, 4, FunctionalState.ENABLE)
    PWM_ResetCounter(LPC_PWM1)
    PWM_CounterCmd(LPC_PWM1, FunctionalState.ENABLE)
    PWM_Cmd(LPC_PWM1, FunctionalState.ENABLE)
"""
UAV motor speed schematic, with each number representing index of speeds list
        0
        |
    3-------1
        |
        2
returns throttle values for each motor in the range of 0-255
"""

# Entry Point
if __name__ == "__main__":
  roboveroConfig()
  initPWM()
  controller= network_controller()
  while True:
    controller.refresh()

    throttle = ((255 - controller.read_sticks()[3]) -127 )* 2;
    if throttle < 0:
        throttle = 0

#    print "throttle: "
    #print throttle

    out = [0,0,0,0]
    out[0] = throttle
    out[1] = throttle
    out[2] = throttle
    out[3] = throttle

    right = controller.read_sticks()[1]-128;
    up = 128 - controller.read_sticks()[0];

    if math.fabs(right) < 20:
        right = 0
    else:
        if right > 0:
            right = right - 20
        else:
            right = right + 20
        right = right / 7
    

    if math.fabs(up) < 20:
        up = 0
    else:
        if up > 0:
            up = up - 20
        else:
            up = up + 20
        up = up/7

#    print "right: "
#    print right

#    print "up: "
#    print up

    out[0] = out[0] + up;
    out[2] = out[2] - up;

    out[1] = out[1]+right;
    out[3] = out[3]-right;

    for i in range(4):
        if out[i] < 0:
            out[i] = 0
        if out[i] > 255:
            out[i] = 255
        out[i] = 1000 + (out[i] /255.0)*1000

#    print out
    PWM_MatchUpdate(LPC_PWM1, 1, out[0], PWM_MATCH_UPDATE_OPT.PWM_MATCH_UPDATE_NEXT_RST)
    PWM_MatchUpdate(LPC_PWM1, 2, out[1], PWM_MATCH_UPDATE_OPT.PWM_MATCH_UPDATE_NEXT_RST)
    PWM_MatchUpdate(LPC_PWM1, 5, out[2], PWM_MATCH_UPDATE_OPT.PWM_MATCH_UPDATE_NEXT_RST)
    PWM_MatchUpdate(LPC_PWM1, 4, out[3], PWM_MATCH_UPDATE_OPT.PWM_MATCH_UPDATE_NEXT_RST)