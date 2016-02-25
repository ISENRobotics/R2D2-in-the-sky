import time
from Adafruit_I2C import Adafruit_I2C
# this device has two I2C addresses
DisplayRGB = Adafruit_I2C(0x62)
DisplayText = Adafruit_I2C(0x3e)
dot = [0b00111,\
       0b00101,\
       0b00111,\
       0b00000,\
       0b00000,\
       0b00000,\
       0b00000,\
       0b00000]
       
class LCD():
    def functionset(self):
        DisplayText.write8(0x20,0b00111100)
        
    def displaycontrol(self):
        DisplayText.write8(0x08, 0b11110000)
        
    def displayclear(self):
        DisplayText.write8(0x01, 100000000)
        
    def entrymodeset(self):
        DisplayText.write8(0x04, 111000000)
        
    def setText(self,texte):
        DisplayText.write8(0x80,0x01)
        time.sleep(.05)
        DisplayText.write8(0x80,0x08 | 0x04)
#        DisplayText.write8(0x80,0x04)
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
        
    def createChar(self, location, charmap):
        data = [0 for i in range(10)]
        for i in range(0,8):
            data[i] = charmap[i]
        data.insert(0,(0x40|(location<<4)))
        data.insert(1,0x40)
        DisplayText.writeList(0x80,data)
            
if __name__=="__main__":
    ecran=LCD()
    ecran.setRGB(255,255,255)
    ecran.createChar(0,dot)
    ecran.functionset()
    time.sleep(1)
#    ecran.functionset()
#    time.sleep(1)
#    ecran.functionset()
#    time.sleep(1)
#    ecran.functionset()
#    time.sleep(1)
#    ecran.displaycontrol()
#    time.sleep(1)
#    ecran.displayclear()
#    time.sleep(2)
#    ecran.entrymodeset()
    
    while True:
        ecran.setText("Hello")
	for c in range(0,255):
		time.sleep(0.02)
        ecran.setRGB(255,0,255)
        time.sleep(1)
        ecran.setRGB(255,255,0)
        time.sleep(1)
        ecran.setRGB(0,255,255)
        time.sleep(1)
