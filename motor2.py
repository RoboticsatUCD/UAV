#Evan Racah, Boris Poutivski
#from custom_servo import initPulse, initPeriod, initPWM
#Expanded functionality from the motor.py class
#Easier to work with imo, but redundant information in each instance of class
#
#Usage:
#from motor2.py include Motor, initMotors
#
#mot1 = Motor(1)
#mot2 = Motor(2)
#mot3 = Motor(3)
#mot1.initAll()
#mot1.setSpeed(500) #half speed


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

def initPWM():
    initPeriod(20000)
    PWM_ResetCounter(LPC_PWM1)
    PWM_CounterCmd(LPC_PWM1, FunctionalState.ENABLE)
    PWM_Cmd(LPC_PWM1, FunctionalState.ENABLE)




class Motor(object):
    motors = []

    def __init__(self,port_number,vmin=0,vmax=1000,speed=0):
        motors.append(self)
        self.setDataMembers(port_number,vmin,vmax,speed)
        initPulse(port_number, 1000)
        PWM_ChannelCmd(LPC_PWM1, port_number, FunctionalState.ENABLE)
        
    def initController():
        self.setSpeed(1000)
        time.sleep(1)
        self.setSpeed(0)
        time.sleep(1)
        
    def initAll():
        initPWM()
        for i in motors:
            i.initController()

    def setDataMembers(port_number,vmin,vmax,speed):
        self.port = port_number
        self.speed = speed
        self.min_speed = vmin
        self.max_speed = vmax

    def setSpeed(self,speed):
        if speed <= self.max_speed or speed >= self.min_speed:
            self.speed=speed
            PWM_MatchUpdate(LPC_PWM1, self.port, self.speed+1000, PWM_MATCH_UPDATE_OPT.PWM_MATCH_UPDATE_NEXT_RST)
        else:
            print "Invalid speed of: " + speed + ", using previous speed of: " + self.speed