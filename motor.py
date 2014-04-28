#Evan Racah
#from custom_servo import initPulse, initPeriod, initPWM

from robovero.LPC17xx import LPC_PWM1
from robovero.lpc17xx_pwm import PWM_TC_MODE_OPT, \
                    PWM_MATCH_UPDATE_OPT, PWM_MATCHCFG_Type, \
                    PWM_MatchUpdate, PWM_ConfigMatch, PWM_ChannelCmd, \
                    PWM_ResetCounter, PWM_CounterCmd, PWM_Cmd
from robovero.extras import roboveroConfig, initMatch
from robovero.lpc_types import FunctionalState

from robovero.arduino import analogWrite, PWM1
import time

def initPulse(channel, pulse_width):
    initMatch(channel, pulse_width)
    
def initPeriod(period):
    initMatch(0, period)

def initMotors():
    initPeriod(20000)
    PWM_ResetCounter(LPC_PWM1)
    PWM_CounterCmd(LPC_PWM1, FunctionalState.ENABLE)
    PWM_Cmd(LPC_PWM1, FunctionalState.ENABLE)




class Motor(object):
    def __init__(self,port_number,vmin=0,vmax=1000,speed=0):
        self.setDataMembers(port_number,vmin,vmax,speed)
        initPulse(port_number, 1000)
        PWM_ChannelCmd(LPC_PWM1, port_number, FunctionalState.ENABLE)
        
    def lowHighInit():
        self.setSpeed(1000)
        self.go()
        time.sleep(1)
        self.setSpeed(0)
        self.go()
        time.sleep(1)

    def setDataMembers(port_number,vmin,vmax,speed):
        self.port = port_number
        self.speed = speed
        self.min_speed = vmin
        self.max_speed = vmax


    def setSpeed(self,speed):
        if speed <= self.max_speed or speed >= self.min_speed:
            self.speed=speed
        else:
            print "Invalid speed of: " + speed + ", using previous speed of: " + self.speed

    def go(self):
        PWM_MatchUpdate(LPC_PWM1, self.port, self.speed+1000, PWM_MATCH_UPDATE_OPT.PWM_MATCH_UPDATE_NEXT_RST)
