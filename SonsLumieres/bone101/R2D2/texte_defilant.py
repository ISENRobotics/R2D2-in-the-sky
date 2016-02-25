import time
from Adafruit_I2C import Adafruit_I2C



# this device has two I2C addresses
DisplayRGB = Adafruit_I2C(0x62)
DisplayText = Adafruit_I2C(0x3e)

       

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
        
        continuer=1
        while continuer == 1:
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
                
                
                if row == 1:
                    if count==16:
                        if len(texte)>31:
                            continuer=1
                            i=0
                            while i<len(texte): 
                                if texte[i]==' ':
                                    texte=texte[i+1:]
                                    break
                                else:
                                    i+=1
                            time.sleep(2)
                else:
                   continuer=0
            
            
            
        
    def setRGB(self, r,g,b):
        DisplayRGB.write8(0,0)
        DisplayRGB.write8(1,0)
        DisplayRGB.write8(2,b)
        DisplayRGB.write8(3,g)
        DisplayRGB.write8(4,r)
        DisplayRGB.write8(8,0xaa)
        
        
    def setToto(self, texte):    
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


if __name__=="__main__":
    ecran=LCD(DisplayText, DisplayRGB)
    ecran.setRGB(255,255,255)
    
    
    while True:
        ecran.setRGB(0,255,255)
        ecran.setToto("du cote obscur ne pas sombrer il faut")
        time.sleep(2)

                
        
        
        
        