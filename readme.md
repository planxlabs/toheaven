# PyC Basic 
## libaray
```python
from pop import Leds
from pop import Switches
from pop import Psd
from pop import Cds
from pop import Sound
from pop import Potentiometer
from pop import PiezoBuzzer
from pop import PixelDisplay
from pop import Sht20
from pop import Gesture
from pop import Oled
import time
</code>
```
## Leds
```python
leds = Leds()
leds.allOn()
leds.allOff()
leds[0].on()
leds[0].off()
```

## Switches
```python
sw = Switches()
r0 = sw[0].read()
r1 = sw[1].read()
print(r0, r1)
```

## Psd
```python
psd = Psd()
r = psd.calcDist(psd.readAverage())
print(r)
```

## Cds
```python
cds = Cds()
r = cds.readAverage()
print(r)
```

## Sound
```python
sound = Sound()
for i in range(100):
    val = sound.read()
    print(val)
```

## Potentiometer
```python
poten = Potentiometer()
r = poten.readVoltAverage()
print(r)
```

## PiezoBuzzer
```python
buzzer = PiezoBuzzer()
buzzer.setTempo(120)
buzzer.tone(4, 8, 4) #octave, pitch duration
```

## PixelDisplay
```python
pixel = PixelDisplay()
pixel.setBrightness(255) 
pixel.setColor(0, 0, [5, 0, 0]) #x, y, color(R:8bit, G:8bit, B:8bit)
time.sleep(3) #second
pixel.fill([255, 0, 255]) #all color
time.sleep(3) #second
pixel.fill([0, 0, 0])
```

## Sht20
```python
sht = Sht20()
t = sht.readTemp()
h = sht.readHumi()
print(t, h)
```

## Gesture
```python
gesture = Gesture()
for i in range(0,1000):
    if gesture.isAvailable():        
        motion = gesture.readStr()
        print(motion) 
    time.sleep(0.1)
```

## Oled
```python
oled = Oled()
oled.setCursor(50, 50)
oled.print("Hello World")
```

