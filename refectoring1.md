> original: https://github.com/respeaker/pixel_ring/blob/master/pixel_ring/usb_pixel_ring_v2.py
```python
import usb.core
import usb.util

VID = 0x2886
PID = 0x0018

class FoundNotAudio(Exception): pass

hex2rgb = lambda n: ((n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF)
rgb2invert = lambda r, g, b: (~r & 0xFF, ~g & 0xFF, ~b & 0xFF)

class AudioPixelRing:

    def __init__(self, brightness=10):
        self.dev = usb.core.find(idVendor=VID, idProduct=PID)
        if not self.dev:
            raise FoundNotAudio
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

    def normal(self, *color):
        r, g, b = hex2rgb(*color) if len(color) == 1 else color 
        self.__write(1, [r, g, b, 0])

    def off(self):
        self.normal(0x000000)
    
    def listen(self, *palette):
        self.__write(0)
        if palette:
            self.__palette(*palette)

    def aurora(self, *palette):
        self.__write(3)
        if palette:
            self.__palette(*palette)

    def think(self, *palette):
        self.__write(4)
        if palette:
            self.__palette(*palette)

    def spin(self, *color):
        self.__write(5)
        if color:
            color = (color[0], ~color[0]) if len(color) == 1 else (color, rgb2invert(*color))
            self.__palette(*color)

    def brightness(self, val):
        self.__write(0x20, [val])
```
