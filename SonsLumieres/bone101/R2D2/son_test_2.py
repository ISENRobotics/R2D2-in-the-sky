import math
import numpy as np
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time


Fe=44100;
t=np.linspace(0,33984/Fe, 33984)


f0=19500
df0=300
A=0.25
B= np.exp(1j*2*math.pi*(f0+df0*t*Fe/(2*33984)-df0/2)*t)
signal0=A*B*np.array([0]*525+[1]*500+[0]*(33984-1025))




f1=8750
df1=500
B= np.exp(1j*2*math.pi*(f1+df1*t*Fe/(2*33984)-df1/2)*t)
signal1=A*B*np.array([0]*1850+[1]*1300+[0]*(33984-3150))

f2=3100
df2=500
B= np.exp(1j*2*math.pi*(f2+df2*t*Fe/(2*33984)-df2/2)*t)
signal2=A*B*np.array([0]*4940+[1]*1300+[0]*(33984-4940-1300))

f3=1275
df3=500
B= np.exp(1j*2*math.pi*(f3+df3*t*Fe/(2*33984)-df3/2)*t)
signal3=A*B*np.array([0]*8820+[1]*1100+[0]*(33984-8820-1100))

f4=625
df4=500
B= np.exp(1j*2*math.pi*(f4+df4*t*Fe/(2*33984)-df4/2)*t)
signal4=A*B*np.array([0]*10580+[1]*1200+[0]*(33984-10580-1200))

f5=620
df5=600
B= np.exp(1j*2*math.pi*(f5+df5*t*Fe/(2*33984)-df5/2)*t)
signal5=A*B*np.array([0]*13760+[1]*1100+[0]*(33984-13760-1100))

f6=968
df6=500
B= np.exp(1j*2*math.pi*(f6+df6*t*Fe/(2*33984)-df6/2)*t)
signal6=A*B*np.array([0]*15200+[1]*1400+[0]*(33984-15200-1400))

f7=962
df7=500
B= np.exp(1j*2*math.pi*(f7+df7*t*Fe/(2*33984)-df7/2)*t)
signal7=A*B*np.array([0]*17370+[1]*1400+[0]*(33984-17370-1400))

f8=955
df8=500
B= np.exp(1j*2*math.pi*(f8+df8*t*Fe/(2*33984)-df8/2)*t)
signal8=A*B*np.array([0]*19800+[1]*1400+[0]*(33984-19800-1400))

f9=947
df9=500
B= np.exp(1j*2*math.pi*(f9+df9*t*Fe/(2*33984)-df9/2)*t)
signal9=A*B*np.array([0]*22500+[1]*1400+[0]*(33984-22500-1400))

f10=2500
df10=500
B= np.exp(1j*2*math.pi*(f10+df10*t*Fe/(2*33984)-df10/2)*t)
signal10=A*B*np.array([0]*25670+[1]*1300+[0]*(33984-25670-1300))

f11=2400
df11=500
B= np.exp(1j*2*math.pi*(f11+df11*t*Fe/(2*33984)-df11/2)*t)
signal11=A*B*np.array([0]*27300+[1]*1300+[0]*(33984-27300-1300))

f12=8000
df12=500
B= np.exp(1j*2*math.pi*(f12+df12*t*Fe/(2*33984)-df12/2)*t)
signal12=A*B*np.array([0]*29590+[1]*1400+[0]*(33984-29590-1400))

f13=4000
df13=500
B= np.exp(1j*2*math.pi*(f13+df13*t*Fe/(2*33984)-df13/2)*t)
signal13=A*B*np.array([0]*31620+[1]*1700+[0]*(33984-31620-1700))


signal=signal0+signal1+signal2+signal3+signal4+signal5+signal6+signal7+signal8+signal9+signal10+signal11+signal12+signal13

GPIO.setup("P9_22", GPIO.OUT)
def lecture_son(signal):
    for i in range(33984/Fe):
        if signal[i]>0:
            GPIO.output("P9_22", GPIO.HIGH)
        else:
            GPIO.output("P9_22", GPIO.LOW)
        time.sleep(1/Fe)
        
PWM.start("P9_22", 50)
PWM.set_frequency("P9_22", Fe)
tempo=0.3

do=523#261
re=587#293
mi=659#329
fa=698#349
sol=783#391
la=880#440
si=987#493


if __name__ == "__main__":
    while True:
        '''
        PWM.set_frequency("P9_22", mi)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", mi)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", fa)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", sol)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", sol)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", fa)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", mi)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", re)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", do)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", do)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", re)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", mi)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", mi)
        time.sleep(0.45)
        PWM.set_frequency("P9_22", re)
        time.sleep(0.3)
        pause(10)
        PWM.set_frequency("P9_22", re)
        time.sleep(0.6)
        time.sleep(3)
        '''
        
        PWM.set_frequency("P9_22", 4000)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 1046)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 4000)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 1130)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 4000)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 1174)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 4000)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 1215)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 4000)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 1260)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 4000)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 1318)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 4000)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 1410)
        time.sleep(tempo)
        PWM.set_frequency("P9_22", 4000)
        time.sleep(tempo)
        
        
        
