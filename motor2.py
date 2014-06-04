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


from robovero.LPC17xx import LPC_PWM1, LPC_MCPWM
from robovero.lpc17xx_pwm import PWM_TC_MODE_OPT, \
                    PWM_MATCH_UPDATE_OPT, PWM_MATCHCFG_Type, \
                    PWM_MatchUpdate, PWM_ConfigMatch, PWM_ChannelCmd, \
                    PWM_ResetCounter, PWM_CounterCmd, PWM_Cmd
from robovero.lpc17xx_mcpwm import MCPWM_Init, MCPWM_CHANNEL_CFG_Type, \
                      MCPWM_ConfigChannel, MCPWM_DCMode, MCPWM_ACMode, \
                      MCPWM_Start, MCPWM_WriteToShadow, MCPWM_Stop,    \
                      MCPWM_CHANNEL_EDGE_MODE, MCPWM_CHANNEL_PASSIVE_HI, MCPWM_CHANNEL_PASSIVE_LO
from robovero.extras import roboveroConfig, initMatch
from robovero.lpc_types import FunctionalState

from robovero.arduino import analogWrite, PWM1
import time

#Channel setup is needed for the proper setup of MCPWM
periodValue = 600000

ENABLE = FunctionalState.ENABLE
DISABLE = FunctionalState.DISABLE

channelsetup = MCPWM_CHANNEL_CFG_Type()
  
channelsetup.channelType = MCPWM_CHANNEL_EDGE_MODE
channelsetup.channelPolarity = MCPWM_CHANNEL_PASSIVE_HI
channelsetup.channelDeadtimeEnable = DISABLE
channelsetup.channelDeadtimeValue = 0
channelsetup.channelUpdateEnable = ENABLE
channelsetup.channelTimercounterValue = 0
channelsetup.channelPeriodValue = periodValue
channelsetup.channelPulsewidthValue = 0

def initPulse(channel, pulse_width):
    initMatch(channel, pulse_width)
    
def initPeriod(period):
    initMatch(0, period)

def initPWM(): #Initializes both the MCPWM and the regular PWM
    MCPWM_DCMode(LPC_MCPWM, DISABLE, DISABLE, (0))
    MCPWM_ACMode(LPC_MCPWM, DISABLE)
    MCPWM_Start(LPC_MCPWM, ENABLE, ENABLE, ENABLE) #Start all three channels, even if we're not using them I guess
    
    initPeriod(20000)
    PWM_ResetCounter(LPC_PWM1)
    PWM_CounterCmd(LPC_PWM1, ENABLE)
    PWM_Cmd(LPC_PWM1, ENABLE)

class Motor(object):
    motors = []
    
    def __init__(self, portNumber, MC=False, vmin=0, vmax=1000, speed=0):
        self.motors.append(self) #Keeps track of all motors
        if MC:
			MCPWM_Init(LPC_MCPWM)
			self.setDataMembers(portNumber,MC,vmin,vmax,speed,self.setSpeedMC)
			MCPWM_ConfigChannel(LPC_MCPWM, portNumber, channelsetup.ptr)
        else:
            self.setDataMembers(portNumber,MC,vmin,vmax,speed,self.setSpeedNorm)
            initPeriod(20000)
            initPulse(portNumber, 1000)
            PWM_ChannelCmd(LPC_PWM1, portNumber, ENABLE)
            
    def __del__(self):
		MCPWM_Stop(LPC_MCPWM, ENABLE, ENABLE, ENABLE)
        
    def initController(self):
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

    def setDataMembers(self, portNumber, MC, vmin, vmax, speed, myfunction):
        self.port = portNumber
        self.MC = MC
        self.speed = speed
        self.minSpeed = vmin
        self.maxSpeed = vmax
        self.updateFunction = myfunction
        
    def setSpeed(self,speed):
		if speed <= self.maxSpeed or speed >= self.minSpeed:
			self.updateFunction(speed)
		else:
			print "Invalid speed of: " + speed + ", using previous speed of: " + self.speed

    def setSpeedNorm(self,speed):
		self.speed=speed
		PWM_MatchUpdate(LPC_PWM1, self.port, self.speed+1000, PWM_MATCH_UPDATE_OPT.PWM_MATCH_UPDATE_NOW)
    
    def setSpeedMC(self,speed):
		channelsetup.channelPulsewidthValue = speed*(periodValue/20000) + periodValue/20
		MCPWM_WriteToShadow(LPC_MCPWM, self.port, channelsetup.ptr)
