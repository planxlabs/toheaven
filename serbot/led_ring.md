# Library (PixelRing.py)
```python
import usb.core
import usb.util

VID = 0x2886
PID = 0x0018

class FoundNotDevice(Exception): pass

hex2rgb = lambda n: ((n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF) 
rgb2invert = lambda r, g, b: (~r & 0xFF, ~g & 0xFF, ~b & 0xFF)

class PixelRing:

    def __init__(self, brightness=10):
        self.dev = usb.core.find(idVendor=VID, idProduct=PID)
        if not self.dev:
            raise FoundNotDevice
        self.brightness(brightness)

    def __del__(self):
        usb.util.dispose_resources(self.dev)
        del self.dev
    
    def __write(self, cmd, data=[0]):
        self.dev.ctrl_transfer(
                usb.util.CTRL_OUT | 
                usb.util.CTRL_TYPE_VENDOR | 
                usb.util.CTRL_RECIPIENT_DEVICE,
                0, cmd, 0x1C, data, 8000
                )
    
    write = __write

    def __palette(self, a, b):
        r1, g1, b1, r2, g2, b2 = *(hex2rgb(a) if (not type(a) is tuple) else a), *(hex2rgb(b) if (not type(b) is tuple) else b) 
        self.__write(0x21, [r1, g1, b1, 0, r2, g2, b2, 0])

    def __pattern(self, cmd, *palette):
        self.__write(cmd)
        if palette:
            self.__palette(*palette)

    def normal(self, *color):
        r, g, b = hex2rgb(*color) if len(color) == 1 else color 
        self.__write(1, [r, g, b, 0])
                
    def off(self):
        self.normal(0x000000)
    
    def listen(self, *palette):
        self.__pattern(0, *palette)

    def aurora(self, *palette):
        self.__pattern(3, *palette)

    def think(self, *palette):
        self.__pattern(4, *palette)

    def spin(self, *color):
        self.__pattern(5, None if not color else *(color[0], ~color[0]) if len(color) == 1 else (color, rgb2invert(*color)))
        
    def brightness(self, val):
        self.__write(0x20, [val])
```
# Test
```python
from AudioPixelRing import PixelRing
import time

pr = PixelRing()

pr.aurora((255,0,0,0),(0,0,255))
time.sleep(5)
pr.normal(128,128,0)
time.sleep(5)
pr.off()
```
