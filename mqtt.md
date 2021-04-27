# MQTT Example

## to publish
```python
import paho.mqtt.client as mqtt

def publish_message():
    data = input("Enter message: ")
    client.publish("SODA/hello", data)

def do_connect(client, userdata, flags, rc):
    print("ok connect")
    publish_message()

def do_publish(client, userdata, mid):
    print("ok publish")
    publish_message()

client = mqtt.Client()

client.on_connect = do_connect
client.on_publish = do_publish
client.connect("192.168.101.101")  #실제 브로커 주소 사용
client.loop_forever()
```

## from subscribe
```python
import paho.mqtt.client as mqtt

def do_connect(client, userdata, flags, rc):
    print("ok connect")
    client.subscribe("hello/world")

def do_message(client, userdata, message):
    print("[%s] %s"%(message.topic, message.payload.decode()))
client = mqtt.Client()

client.on_connect = do_connect
client.on_message = do_message

client.connect("192.168.101.101")  

client.loop_forever()
```

## Chatting
```python
import paho.mqtt.client as mqtt
import threading

nic_name = None
def __task_publish(client):
    topic = "hello/" + nic_name + "/chat"
    data = input()
    client.publish(topic, data)

def do_connect(client, usrdata, flags, rc):
    if rc == 0:
        print("hi~ %s"%(nic_name))
        client.subscribe("hello/+/chat") 
        threading.Thread(target=__task_publish, args=(client,)).start()
    else:
        print("not connect")

def do_publish(client, usrdata, mid):
    threading.Thread(target=__task_publish, args=(client,)).start()![image](https://user-images.githubusercontent.com/42823673/116172298-6f7d5980-a745-11eb-8fe9-740530c17838.png)

def do_message(client, usrdata, message):
    t_nic_name = message.topic.split('/')[1]
    if nic_name != t_nic_name:
        print(' ' * 40, "[%s] %s"%(t_nic_name, message.payload.decode()))

def main():
    global nic_name
    
    nic_name = input("your nic name: ")

    client = mqtt.Client()
    client.on_connect = do_connect
    client.on_publish = do_publish
    client.on_message = do_message
    client.connect("192.168.101.101") #실제 브로커 주소 사용
    client.loop_forever()

if __name__ == "__main__":
    main()
![image](https://user-images.githubusercontent.com/42823673/116172321-7efca280-a745-11eb-8980-795aa721cc2a.png)

```

## IoT 
### Target
```python
import paho.mqtt.client as mqtt
import subprocess
import json

id = None

def do_connect(client, usrdata, flags, rc):
    if rc == 0:
        print("ok connect")
        client.subscribe("SODA/led/action") 
    else:
        print("not connect")

def do_message(client, usrdata, message):
    led_info = json.loads(message.payload)

    if id != led_info['id']:
        return
        
    if led_info['action'] == 'on':
        // ref led_info['led']
    elif led_info['action'] == 'off':
        // ref led_info['led']
        
    client.publish("SODA/led/state", "id:%d, led:%d, state:%s"%(id, led_info['led'], led_info['action']))

def main():
    global id

    id = int(input("input your id: "))

    client = mqtt.Client()
    client.on_connect = do_connect
    client.on_message = do_message
    client.connect("192.168.101.101") 
    client.loop_forever()

if __name__ == "__main__":
    main()
```

### Host
```python
import paho.mqtt.client as mqtt
import threading
import json

def __task_publish(client):
    led_info = {'id':None, 'led':None, 'action':None}

    led_info['id'] = int(input("Target ID: "))
    led_info['led'] = int(input("LED: "))
    led_info['action'] = input("Action: ")
    client.publish("SODA/led/action", json.dumps(led_info))

def do_connect(client, usrdata, flags, rc):
    if rc == 0:
        print("ok connect")
        client.subscribe("SODA/led/state") 
        threading.Thread(target=__task_publish, args=(client,)).start()
    else:
        print("not connect")

def do_publish(client, userdata, mid):
    threading.Thread(target=__task_publish, args=(client,)).start()

def do_message(client, usrdata, message):
    print(' ' * 20, "<<<", message.payload.decode())

def main():
    client = mqtt.Client() 
    client.on_connect = do_connect
    client.on_publish = do_publish
    client.on_message = do_message
    client.connect("192.168.101.101")  #실제 브로커 주소 사용
    client.loop_forever()

if __name__ == "__main__":
    main()
```
