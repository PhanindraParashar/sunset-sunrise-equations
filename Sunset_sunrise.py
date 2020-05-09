import numpy as np
import matplotlib.pyplot as plt
import time 
import datetime

pi = np.pi


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


# All data at UTC
P2019 = '03-01-2019 7:43:0'
AE2018 = '22-09-2018 01:54:0'
lamp = theta(DateDelta(AE2018,P2019))
e = 0.0167
T = 365.256363

date = '05-08-2019 00:00:00'
days = DateDelta(P2019,date)

def M(t):
    return (2*np.pi/T)*t

def theta(t):
    E = solve_ar(t)
    term_rec = ((1-e)/(1+e))**.5
    theta = 2*arctan(tan(E/2)*term_rec)
    if theta < 0:
        theta = theta + 360
    return theta

def solve_ar(t):
    ar = M(t)
    E0 = ar
    for i in range(10):
        fx = E0 - e*np.sin(E0) - ar
        fd = 1 - e*np.cos(E0)
        h = -fx/fd
        E0 = E0 + h
    return E0*180/np.pi

    

def sunset (days,Lt,Ln,altitude,UTC):
    # for 2019 
    M = .98560028*(days - (Ln/360)) - 3.3883357
    while M >= 360:
        M = M -360
    
    C = 1.9148*sin(M) + 0.02*sin(2*M) + 0.0003*sin(3*M)
      
    lam = (M+C+180+102.9372)
    lam = 180 + theta(days) + lamp
    
    while lam >= 360:
        lam = lam - 360
    
    
    
    delta = arcsin(sin(lam)*sin(23.44))
    
    ref = -.83 - (2.076/60)*np.sqrt(altitude)
    
    t1 = sin(ref)/(cos(delta)*cos(Lt))
    t2 = tan(delta)*tan(Lt)
    
    w0 = arccos(t1-t2)
    
    long_corr = 4*(Ln - 15*UTC)
    Eot_corr = 9.87*sin(2*lam) - 7.53*cos(lam) + 1.5*sin(lam)
    
#    B = 360*(days-81)/365
#    B = B*np.pi/180
#    Eot_corr = 9.87*np.sin(2*B) - 7.53*np.cos(B) + 1.5*np.sin(B)
    
    sol_cor = (long_corr - Eot_corr)/60
    
    
    hrs = w0/15 - sol_cor

    print(lam,M,C)
    return hms(hrs)

def cal(E,e):
    M = E - e*sin(E)
    term = np.sqrt((e+1)/(1-e))
    nu = 2*arctan(term*tan(E/2))
    return M,nu,nu-M







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

def actual_z(measured,hm):
    return arccos(cos(measured) - sin(.83 + (2.076/60)*np.sqrt(hm)))


