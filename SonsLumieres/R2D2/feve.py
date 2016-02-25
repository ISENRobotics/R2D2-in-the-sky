import time
import numpy as np
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.PWM as PWM

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

CLK_PIN = "P9_26"
DATA_PIN = "P9_24"
NUMBER_OF_LEDS = 2

DisplayRGB = Adafruit_I2C(0x62)
DisplayText = Adafruit_I2C(0x3e)


def jouer_note(note, duty):
    PWM.set_frequency("P9_22", note)
    PWM.set_duty_cycle("P9_22", duty)
    time.sleep(0.5)
    PWM.set_duty_cycle("P9_22", 0)
    time.sleep(0.3)
    PWM.set_duty_cycle("P9_22", duty)



class ChainableLED():
    def __init__(self, clk_pin, data_pin, number_of_leds):
        self.__clk_pin = clk_pin
        self.__data_pin = data_pin
        self.__number_of_leds = number_of_leds
 
        GPIO.setup(self.__clk_pin, GPIO.OUT)
        GPIO.setup(self.__data_pin, GPIO.OUT)
        
        self.tab = np.zeros((9,), dtype=np.byte)
 
        for i in range(self.__number_of_leds):
            self.setColorRGB(i, 0, 0, 0)
 
    def clk(self):
        GPIO.output(self.__clk_pin, GPIO.LOW)
        time.sleep(0.00002)
        GPIO.output(self.__clk_pin, GPIO.HIGH)
        time.sleep(0.00002)
 
    def sendByte(self, b):
        "Send one bit at a time, starting with the MSB"
        for i in range(8):
            # If MSB is 1, write one and clock it, else write 0 and clock
            if (b & 0x80) != 0:
                GPIO.output(self.__data_pin, GPIO.HIGH)
            else:
                GPIO.output(self.__data_pin, GPIO.LOW)
            self.clk()
 
            # Advance to the next bit to send
            b = b << 1
 
    def sendColor(self, red, green, blue):
        "Start by sending a byte with the format '1 1 /B7 /B6 /G7 /G6 /R7 /R6' "
        #prefix = B11000000
        prefix = 0xC0
        if (blue & 0x80) == 0:     
            #prefix |= B00100000
            prefix |= 0x20
        if (blue & 0x40) == 0:     
            #prefix |= B00010000
            prefix |= 0x10
        if (green & 0x80) == 0:    
            #prefix |= B00001000
            prefix |= 0x08
        if (green & 0x40) == 0:    
            #prefix |= B00000100
            prefix |= 0x04
        if (red & 0x80) == 0:      
            #prefix |= B00000010
            prefix |= 0x02
        if (red & 0x40) == 0:      
            #prefix |= B00000001
            prefix |= 0x01
        self.sendByte(prefix)
 
        # Now must send the 3 colors
        self.sendByte(blue)
        self.sendByte(green)
        self.sendByte(red)
 
    def setColorRGB(self, led, red, green, blue):
        # Send data frame prefix (32x '0')
        self.sendByte(0)
        self.sendByte(0x00)
        self.sendByte(0)
        self.sendByte(0)

 
        # Send color data for each one of the leds
        for i in range(self.__number_of_leds):
            '''
            if i == led:
                _led_state[i*3 + _CL_RED] = red;
                _led_state[i*3 + _CL_GREEN] = green;
                _led_state[i*3 + _CL_BLUE] = blue;
            sendColor(_led_state[i*3 + _CL_RED], 
                      _led_state[i*3 + _CL_GREEN], 
                      _led_state[i*3 + _CL_BLUE]);
            '''
            if i == led:
                self.tab[i*3 + 0] = red;
                self.tab[i*3 + 1] = green;
                self.tab[i*3 + 2] = blue;
            
            self.sendColor(self.tab[i*3 + 0], self.tab[i*3 + 1], self.tab[i*3 + 2])
                #self.send()
 
        # Terminate data frame (32x "0")
        self.sendByte(0)
        self.sendByte(0)
        self.sendByte(0x00)
        self.sendByte(0x00)
        
        
        
class LCD():
    def __init__(self,DisplayText, DisplayRGB):
        time.sleep(0.030)
        DisplayText.write8(0x80,0x20 | 0x08 |0x04)
        time.sleep(0.00004)
        DisplayText.write8(0x80, 0x08 | 0x04 | 0x02 | 0x01)#display
        time.sleep(0.00004)
        DisplayText.write8(0x80, 0x01)#clear
        time.sleep(0.0016)
        DisplayText.write8(0x80, 0x04 | 0x02 | 0x00)
        time.sleep(1)
        
    def setText(self,texte):
        DisplayText.write8(0x80,0x01)
        time.sleep(.05)
        DisplayText.write8(0x80,0x08 | 0x04)
        DisplayText.write8(0x80,0x28)
        time.sleep(.05)
        
        compteur=0
        if len(texte)>31:
            i=0
            while i<len(texte): 
                if texte[i]==' ':
                    compteur+=1
                i+=1
                    
        cptr=0
        while cptr<compteur+1:
            DisplayText.write8(0x80, 0x01)
            time.sleep(0.002)
            count = 0
            row = 0
            
            for c in texte:
                if c == '\n' or count == 16:
                    count = 0
                    row += 1
                    if row == 2:
                        break
                    DisplayText.write8(0x80,0xc0)
                    if c == '\n':
                        continue
                  
                count += 1
                DisplayText.write8(0x40,ord(c))
                
                

            i=0
            while i<len(texte): 
                if texte[i]==' ':
                    texte=texte[i+1:]
                    break
                else:
                    i+=1
                    time.sleep(0.3)

            cptr+=1
        
    def setRGB(self, r,g,b):
        DisplayRGB.write8(0,0)
        DisplayRGB.write8(1,0)
        DisplayRGB.write8(2,b)
        DisplayRGB.write8(3,g)
        DisplayRGB.write8(4,r)
        DisplayRGB.write8(8,0xaa)
        
    def clear(self):
        DisplayText.write8(0x80, 0x01)#clear
        



    
        
if __name__ == "__main__":
    rgb_led = ChainableLED(CLK_PIN, DATA_PIN, NUMBER_OF_LEDS)
    ecran=LCD(DisplayText, DisplayRGB)
    ecran.setRGB(255,255,255)

 
    rgb_led.setColorRGB(0, 255, 255, 0)
    rgb_led.setColorRGB(1, 255, 255, 0)
    #ecran.setText("J'ai eu la feve!")
    ecran.setText("Zut!Encore rate!\n      #ISEN")