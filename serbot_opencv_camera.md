# SerBot Opencv camera (cam.py)
```python
import cv2

cam_cmd = lambda cam_with=1280, cam_height=720, win_with=1280, win_height=720, rate=30, flip=0 : ('nvarguscamerasrc ! '
            'video/x-raw(memory:NVMM), '
            'width={0}, height={1}, '
            'format=NV12, framerate={2}/1 ! '
            'nvvidconv flip-method={3} ! '
            'video/x-raw, width={4}, height={5}, '
            'format=BGRx ! '
            'videoconvert ! appsink').format(cam_with, cam_height, rate, flip, win_with, win_height)

cam = cv2.VideoCapture(cam_cmd(), cv2.CAP_GSTREAMER)
if cam.isOpened() == False:
    print ('Can\'t open the CAM(%d)' % (0))
    exit()

while(True):
    ret, frame = cam.read()
    cv2.imshow("preview", frame)
    if cv2.waitKey(10) >= 0:
        break

cam.release()
cv2.destroyWindow('preview')
```
