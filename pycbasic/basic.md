# PyC Baisc Example with Pop Library
```python
from pop import Leds, PiezoBuzzer, Oled, PixelDisplay
from pop import Switches, Potentiometer, Sound, Cds, TempHumi, Psd, Gesture
from pop import Sht20 as TempHumi
from pop import PopThread

import time

def led_test():
    leds = Leds()
    leds.allOn()
    time.sleep(1)
    leds.allOff()
    time.sleep(1)

    for i in range(8):
        leds[i].on()
        time.sleep(.5)
        leds[i].off()
        time.sleep(.5)


def piezo_buzzer_test():
    buzzer = PiezoBuzzer()
    
    buzzer.setTempo(120)
    buzzer.tone(4, 1, 4)
    buzzer.tone(4, 3, 4)
    buzzer.tone(4, 5, 4)
    buzzer.tone(4, 6, 4)
    buzzer.tone(4, 8, 4)
    buzzer.tone(4, 10, 4)
    buzzer.tone(4, 12, 4)
    buzzer.tone(5, 1, 4)

    
def oled_test():
    oled = Oled()
    
    print(oled.width(), oled.height())
    
    oled.drawCircle(60,30,10,oled.WHITE)
    time.sleep(1)
    oled.fillCircle(60,30,10,oled.WHITE)
    time.sleep(1)
    oled.clearDisplay()

    
def pixel_display_test():
    pixel = PixelDisplay()
    
    pixel.setBrightness(50)
    pixel.fill([255,0,0])
    time.sleep(1)
    
    pixel.setBrightness(255)
    for y in range(8):
        for x in range(8):
            pixel.setColor(x, y, [255,255,0])
            time.sleep(.1)
    
    pixel.rainbow()
    pixel.clear()


def on_switch(sw):
    print("sw2 press" if sw.read() else "sw2 unpress")
    
def switchs_test():
    from pop import Switch, Input
    sw1 = Switch(7, True) # Bug (disable interrupted)
    sw2 = Switch(27, True)
    sw2.setCallback(on_switch, sw2)
    
    sw1_old = False
    while True:
        try:
            ret = sw1.read()
            if sw1_old != ret:
                sw1_old = ret
                print("sw1 press" if ret else "sw1 unpress")
            time.sleep(.1)
        except KeyboardInterrupt:
            break
        
def on_potentiometer(val):
    print("%d"%(val))
    time.sleep(.1)

def potentiometer_test():
    poten = Potentiometer()
    poten.setRangeTable([144, 629, 1112, 1621, 2085, 2642, 3158, 3590, 3992, 4094])
        
    poten.setCallback(on_potentiometer)
    input("Press <ENTER> key...\n")
    poten.stop()


def on_sound(val):
    ret = abs(val - (4096//2 + 12))
    if ret > 10:
        print(ret)
    
def sound_test():
    sound = Sound()
    
    sound.setCallback(on_sound, type=Sound.TYPE_AVERAGE)
    input("Press <ENTER> key...\n")
    sound.stop()


def on_cds(val):
    print(val)

def cds_test():
    cds = Cds()
    
    cds.setCallback(on_cds, type=Cds.TYPE_AVERAGE)
    input("Press <ENTER> key...\n")
    cds.stop()
    

def temp_humi_test():
    temphumi = TempHumi()

    while True:
        try:
            print(round(temphumi.readTemp(),1), round(temphumi.readHumi(),1))    
            time.sleep(.5)
        except KeyboardInterrupt:
            break
    

def on_psd(psd):
    def wrapper(val):
        print(psd.calcDist(val), "cm")
        time.sleep(.1)
    return wrapper

def psd_test():
    psd = Psd()

    psd.setCallback(on_psd(psd))
    input("Press <ENTER> key...\n")  
    psd.stop()


class MyGesture(PopThread):
    def __init__(self):
        self.__gesture = Gesture()
        
    def run(self):
        if self.__gesture.isAvailable():
            print(self.__gesture.read())

def gesture_test():
    gesture = MyGesture()
    
    gesture.start()
    input("Press <ENTER> key...\n")  
    gesture.stop()
    
        
if __name__ == "__main__":
    pass
```
