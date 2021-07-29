```python
cam_cmd = lambda cam_with=1280, cam_height=720, win_with=1280, win_height=720, rate=30, flip=0 : ('nvarguscamerasrc ! '
            'video/x-raw(memory:NVMM), '
            'width={0}, height={1}, '
            'format=NV12, framerate={2}/1 ! '
            'nvvidconv flip-method={3} ! '
            'video/x-raw, width={4}, height={5}, '
            'format=BGRx ! '
            'videoconvert ! appsink').format(cam_with, cam_height, rate, flip, win_with, win_height)
```
