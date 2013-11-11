#Evan Racah
from custom_servo import initPulse, initPeriod, initPWM

from robovero.LPC17xx import LPC_PWM1
from robovero.lpc17xx_pwm import PWM_TC_MODE_OPT, \
                    PWM_MATCH_UPDATE_OPT, PWM_MATCHCFG_Type, \
                    PWM_MatchUpdate, PWM_ConfigMatch, PWM_ChannelCmd, \
                    PWM_ResetCounter, PWM_CounterCmd, PWM_Cmd
from robovero.extras import roboveroConfig, initMatch
from robovero.lpc_types import FunctionalState

from robovero.arduino import analogWrite, PWM1

class Motor(object):
    def __init__(self,port_number,vmin,vmax,speed=0):
        self.port=port_number
        self.speed=speed
        self.min_speed=vmin
        self.max_speed=vmax
   
    def setSpeed(self,speed):
        if speed<=self.max_speed or speed>=self.min_speed:
            self.speed=speed
        else:
            pass
            #raise error?
        
    def go(self):
        pulse=self._speed_to_pulse(self.speed)
        #initPulse(port_number,speedToPulse(speed))
        #or
        PWM_MatchUpdate(LPC_PWM1, self.port, pulse, PWM_MATCH_UPDATE_OPT.PWM_MATCH_UPDATE_NEXT_RST)
       
    def _speed_to_pulse(self,speed):
        if speed>=0 and speed<=100:
            return speed*10+1000
        else:
            pass
            #raise error
