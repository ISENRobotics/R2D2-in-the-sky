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
        
    def setRGB(self, r,g,b):
        DisplayRGB.write8(0,0)
        DisplayRGB.write8(1,0)
        DisplayRGB.write8(2,b)
        DisplayRGB.write8(3,g)
        DisplayRGB.write8(4,r)
        DisplayRGB.write8(8,0xaa)
        
    def createChar(self,location, charmap):
        data = [0 for i in range(10)];
        for i in range(0,8):
            data[i] = charmap[i]
        data.insert(0,(0x40|(location<<4)))
        data.insert(1,0x40)
        DisplayText.writeList(0x80,data)

    
            

if __name__=="__main__":
    ecran=LCD(DisplayText, DisplayRGB)
    ecran.setRGB(255,255,255)
    #chr(4: coeur, 2 smiley)
    
    while True:
        ecran.setRGB(255,0,255)
        #ecran.setText("Hello world\nIt is a BBG Demo!")
        time.sleep(1)
        #ecran.setText("   Hello.") 
        ecran.setRGB(255,255,0)
        ecran.setText(chr(4))
        time.sleep(1)
        ecran.setRGB(0,255,255)
        ecran.setText(chr(2))
        time.sleep(1)