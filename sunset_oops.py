import numpy as np
import matplotlib.pyplot as plt
import time 
import datetime

pi = np.pi
# All data at UTC
P2019 = '03-01-2019 7:43:0'
AE2018 = '22-09-2018 01:54:0'
lamp = theta(DateDelta(AE2018,P2019))
e = 0.0167
T = 365.256363

def sin(x):
    return np.sin(x*np.pi/180)
def cos(x):
    return np.cos(x*np.pi/180)
def tan(x):
    return sin(x)/cos(x)

def arcsin(x):
    return np.arcsin(x)*180/np.pi
def arccos(x):
    return np.arccos(x)*180/np.pi
def arctan(x):
    return np.arctan(x)*180/np.pi

def hms(h):
    hi = int(h)
    m = 60*(h - hi)
    mi = int(m)
    sec = (m-mi)*60
    return hi,mi,sec

def DateDelta(d1,d2):
    fmt = '%d-%m-%Y %H:%M:%S'

    date1 = datetime.datetime.strptime(d1,fmt)
    date2 = datetime.datetime.strptime(d2,fmt)
    
    a = time.mktime(date1.timetuple())
    b = time.mktime(date2.timetuple())
    seconds = int(b-a)     #seconds
    minutes = seconds/60
    hrs = minutes/60
    days = hrs/24
    
    return days

class SunSet2019():
    def __init__(self,date,Lt,Ln,alt,UTC):
        
        self.date = date
        self.Lt = Lt
        self.Ln = Ln
        self.alt = alt
        self.UTC = UTC
        self.days = DateDelta(P2019,self.date)
    
    def Time(self):
        M = .98560028*(self.days - (self.Ln/360)) - 3.3883357
        while M >= 360:
            M = M -360
    
        C = 1.9148*sin(M) + 0.02*sin(2*M) + 0.0003*sin(3*M)
        
        lam = (M+C+180+102.9372)
        lam = 180 + theta(self.days) + lamp
        
        while lam >= 360:
            lam = lam - 360
        
    
        
        delta = arcsin(sin(lam)*sin(23.44))
        
        ref = -.83 - (2.076/60)*np.sqrt(self.alt)
        
        t1 = sin(ref)/(cos(delta)*cos(self.Lt))
        t2 = tan(delta)*tan(self.Lt)
        
        w0 = arccos(t1-t2)
        
        long_corr = 4*(self.Ln - 15*self.UTC)
        Eot_corr = 9.87*sin(2*lam) - 7.53*cos(lam) + 1.5*sin(lam)
        sol_cor = (long_corr - Eot_corr)/60
        
        
        hrs = w0/15 - sol_cor
        
        return hms(hrs)
    