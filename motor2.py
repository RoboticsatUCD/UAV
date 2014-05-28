#Evan Racah, Boris Poutivski
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

#If an unprogrammed controller is connected, use
#Connect the controller in question to ground and signal pins on the input cable, but do not connect power
#mot1 = Motor(1)
#mot1.programController()
#Connect the power cable to the controller within 20 seconds
#Wait 20 seconds
#The controller is now connected and configured


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

    def __init__(self, port_number, vmin=0, vmax=1000, speed=0):
        self.motors.append(self)
        self.setDataMembers(port_number,vmin,vmax,speed)
        initPeriod(20000)
        initPulse(port_number, 1000)
        PWM_ChannelCmd(LPC_PWM1, port_number, FunctionalState.ENABLE)
        
    def initController(self):
		print self.port
		self.setSpeed(0)
    
    def programController(self):
        initPWM()
        self.setSpeed(1000)
        time.sleep(20)
        self.setSpeed(0)
        
    
    def initAll(self):
        initPWM()
        for i in self.motors:
            i.initController()
            print "Motor initialized"
        time.sleep(4)

    def setDataMembers(self, port_number, vmin, vmax, speed):
        self.port = port_number
        self.speed = speed
        self.min_speed = vmin
        self.max_speed = vmax

    def setSpeed(self,speed):
        if speed <= self.max_speed or speed >= self.min_speed:
            self.speed=speed
            PWM_MatchUpdate(LPC_PWM1, self.port, self.speed+1000, PWM_MATCH_UPDATE_OPT.PWM_MATCH_UPDATE_NOW)
        else:
            print "Invalid speed of: " + speed + ", using previous speed of: " + self.speed
