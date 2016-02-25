import Adafruit_BBIO.PWM as PWM
import time

do=523#261
re=587#293
mi=659#329
fa=698#349
fad=739
sol=783#391
la=880#440
si=987#493
tempo=0.3
Fe=44100;

def hymne_joie():
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
    PWM.set_frequency("P9_22", re)
    time.sleep(0.6)
    time.sleep(3)
    
def jouer_note(note, duty):
    PWM.set_frequency("P9_22", note)
    PWM.set_duty_cycle("P9_22", duty)
    time.sleep(0.5)
    PWM.set_duty_cycle("P9_22", 0)
    '''    
    lst = range(duty, -1, -1)
    for i in lst:
        PWM.set_duty_cycle("P9_22", i)
        time.sleep(0.008)
    '''
    time.sleep(0.3)
    PWM.set_duty_cycle("P9_22", duty)
    
    
def marche_imperiale():
    #PWM.start("P9_22", 50)
    
    jouer_note(sol, 50)
    jouer_note(sol, 50)
    jouer_note(sol, 50)
    
    PWM.set_frequency("P9_22", mi)
    time.sleep(0.45)
    PWM.set_frequency("P9_22", si)
    time.sleep(0.15)
    PWM.set_frequency("P9_22", sol)
    time.sleep(0.6)
    PWM.set_frequency("P9_22", mi)
    time.sleep(0.45)
    PWM.set_frequency("P9_22", si)
    time.sleep(0.15)
    PWM.set_frequency("P9_22", sol)
    time.sleep(0.45)
    
    PWM.set_duty_cycle("P9_22", 0)
    time.sleep(0.6)
    jouer_note(re,50)
    jouer_note(re,50)
    jouer_note(re,50)
    PWM.set_frequency("P9_22", mi)
    time.sleep(0.45)
    PWM.set_frequency("P9_22", si)
    
    time.sleep(0.15)
    PWM.set_frequency("P9_22", fad)
    time.sleep(0.6)
    PWM.set_frequency("P9_22", mi)
    time.sleep(0.45)
    PWM.set_frequency("P9_22", si)
    time.sleep(0.15)
    jouer_note(sol,50)
    jouer_note(sol,50)
    PWM.set_duty_cycle("P9_22", 0)
    
    
    
    
    
PWM.start("P9_22", 50)
PWM.set_frequency("P9_22", Fe)


if __name__ == "__main__":
    while True:
        #hymne_joie()
        marche_imperiale()
        time.sleep(1)

