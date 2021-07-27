# IMU + XNode (imu_node.py)
```python
from pop import IMU, xnode, time
from serial import Serial

DEBUG = True

imu = IMU()
cmd = b'A'

if DEBUG:
    ser = Serial()

while True:
    data = ""

    if cmd == b'A':    
        for d in imu.accel(), imu.gyro():
            data += ("%.2f," * 3)%(d)
        data += ("%.2f," * 4)%(imu.quat()) 
    elif cmd == b'a':
        data = ("%.2f," * 3)%(imu.accel())
    elif cmd == b'g':
        data = ("%.2f," * 3)%(imu.gyro())
    elif cmd == b'q':
        data = ("%.2f," * 4)%(imu.quat()) 
    else:
        data = "Unknown command"
        
    data += '\n'
    xnode.transmit(xnode.ADDR_COORDINATOR, data)
    if DEBUG:
        ser.write(data)
    
    packet = xnode.receive()
    if packet:
        cmd = packet['payload']
    
    if DEBUG:
        t = ser.read()    
        if t:
            cmd = t
    
    time.sleep(0.1)
```

# XNode Gateway(gateway.py)
```python
from pop import time

ser = Serial()

while True:
    packet = xnode.receive()
    if packet:
        data = packet['payload']
        ser.write(data)
    
    cmd = ser.read()
    if cmd:
        xnode.transmit(xnode.ADDR_BROADCAST, cmd) 
    
    time.sleep(.1)
```

# Serbot + PySerial (imu_app.y)
```python
import serial
import time
from threading import Thread

ser = serial.Serial("/dev/ttyUSB1", 115200) 

def set_cmd():
    while True:
        cmd = input()
        ser.write(cmd.encode())
        time.sleep(.1)

th = Thread(target=set_cmd)
th.daemon = True
th.start()

while True:
    try:
        ret = ser.readline()
        if ret:
            print(ret.decode()[:-2])
    except(KeyboardInterrupt):
        break

ser.close()
```
