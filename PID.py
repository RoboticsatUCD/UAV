'''
Created on Aug 20, 2013

@author: ejracah
'''
import time

class PIDControl(object):
    def __init__(self,setpoint,Kp,Ki=0,Kd=0):
        self.setpoint = setpoint
        self.t1 = time.time()
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.error_total = 0
        self.error = 0
        self.error_prev = 0
        self.max_error = 500
        self.min_error = -500

    def update(self,measurement):
        self.error = max(min((self.setpoint - measurement), self.max_error), self.min_error)
        self.errorTotal = self.error_total + self.error
        self.de = self.error - self.error_prev
        self.error_prev = self.error
        self.dt = time.time() - self.t1
        t1 = time.time()

        self.P = self.Kp * self.error
        self.I = self.Ki * self.error_total * self.dt
        self.D = self.Kd * self.de / self.dt
        
        u=self.P + self.I + self.D
        
        return u

    def set_set_point(self,setpoint):
        self.setpoint=setpoint
