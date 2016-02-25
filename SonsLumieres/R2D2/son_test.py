import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_I2C as I2C
import time


PWM.start("P9_22", 50)
sol=783

if __name__ == "__main__":
   
 
    while True:
        PWM.set_frequency("P9_22", sol)
        lst = range(100, -1, -1)
        for i in lst:
            print(i)
            PWM.set_duty_cycle("P9_22", i)
            time.sleep(0.005)

        