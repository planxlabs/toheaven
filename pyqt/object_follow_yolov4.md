# Pop Modify (append class Object_Fallow2)
> Pilot.py
```python

class Object_Follow:
    ...

class Object_Follow2:
    def __init__(self, camera, width=224, height=224):
        self.default_path = os.path.abspath(__file__+"/../model/yolov4-tiny/")

        self.camera = camera
        self.camera_width = width
        self.camera_height = height
        
        global YOLOv4
        from yolov4.tf import YOLOv4
        self.model = YOLOv4(tiny=True)

        self.model.classes = self.default_path+"/coco.names"
        self.model.input_size = (width, height)

    def __del__(self):
        self.camera.release()

    def load_model(self):
        path = self.default_path + '/yolov4-tiny.weights'

        try:
            self.model.make_model()
            self.model.load_weights(path, weights_type="yolo")
        except Exception as e:
            if e.errno==2:
                print("Can't find pre-trained model file. Please refer https://github.com/hanback-docs/yolov4-tiny")
            else:
                print(e)

    def detect(self, index=None, threshold=0.5, show=True, callback=None):
        ret, image = self.camera.read()
        if not ret:
            raise Exception("can't read camera data")

        self.label_list = list(self.model.classes.values())

        if type(index) == str:
            try:
                index = self.label_list.index(index)
            except ValueError:
                raise Exception("index is not available.")

        width = self.camera_width
        height = self.camera_height

        detections = self.model.predict(image, score_threshold=threshold)

        detections = [[{'label':int(det[4]), 'confidence':det[5], 'bbox':[det[0]-det[2]/2,
                                                                        det[1]-det[3]/2,
                                                                        det[0]+det[2]/2,
                                                                        det[1]+det[3]/2]} 
                    for det in detections if det[5]>=threshold]]
                    
        for det in detections[0]:
            bbox = det['bbox']
            cv2.rectangle(image, (int(width * bbox[0]), int(height * bbox[1])), (int(width * bbox[2]), int(height * bbox[3])), (255, 0, 0), 2)

            label=self.label_list[det['label']]
            label_size=cv2.getTextSize(label,cv2.FONT_HERSHEY_SIMPLEX,0.5,1)[0]

            cv2.rectangle(image, (int(width * bbox[0]), int(height * bbox[1]-label_size[1]-5)), (int(width * bbox[0]+label_size[0]), int(height * bbox[1])), (255, 0, 0), -1)
            cv2.putText(image, label, (int(width * bbox[0]), int(height * bbox[1]-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

        if index is not None:
            matching_detections = [d for d in detections[0] if d['label'] == int(index)]

            det=None
            max_bbox_size=0
            
            for d in matching_detections:
                cur_size=(width*d['bbox'][0]-width*d['bbox'][2])**2+(height*d['bbox'][1]-height*d['bbox'][3])**2
                if max_bbox_size<cur_size :
                    max_bbox_size=cur_size
                    det = d
            
            if det is not None:
                bbox = det['bbox']
                label=self.label_list[det['label']]
                label_size=cv2.getTextSize(label,cv2.FONT_HERSHEY_SIMPLEX,0.5,1)[0]
                cv2.rectangle(image, (int(width * bbox[0]), int(height * bbox[1])), (int(width * bbox[2]), int(height * bbox[3])), (0, 255, 0), 4)
                cv2.rectangle(image, (int(width * bbox[0]-2), int(height * bbox[1]-label_size[1]-5)), (int(width * bbox[0]+label_size[0]), int(height * bbox[1])), (0, 255, 0), -1)
                cv2.putText(image, label, (int(width * bbox[0]), int(height * bbox[1]-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                x = (bbox[0] + bbox[2]) / 2.0 - 0.5
                y = (bbox[1] + bbox[3]) / 2.0 - 0.5
                det_size=abs(width*bbox[0]-width*bbox[2])*abs(height*bbox[1]-height*bbox[3])
                cam_size=width*height
                size=det_size/cam_size
                result = {'x':x, 'y':y, 'size_rate':size}
            else:
                result = None, None

        return result, image
```

# Serbot Example 1 (camera + omni wheel) 
```python
from pop import Pilot 
import cv2

cam_cmd = lambda cam_with=224, cam_height=224, win_with=224, win_height=224, rate=60, flip=0 : ('nvarguscamerasrc ! '
            'video/x-raw(memory:NVMM), '
            'width={0}, height={1}, '
            'format=NV12, framerate={2}/1 ! '
            'nvvidconv flip-method={3} ! '
            'video/x-raw, width={4}, height={5}, '
            'format=BGRx ! '
            'videoconvert ! appsink').format(cam_with, cam_height, rate, flip, win_with, win_height)

cam = cv2.VideoCapture(cam_cmd(), cv2.CAP_GSTREAMER)

bot = Pilot.SerBot() 

of = Pilot.Object_Follow2(cam)
of.load_model()

print(">>>", "Successful model...")

while True:
    try:
        h, _ = of.detect(index='person')
        print('###', h)
        
        if h is not None: 
            steer = h['x'] * 4 
            if steer > 1:
                steer = 1
            elif steer < -1:
                steer = -1
            
            bot.steering = steer

            if h['size_rate'] < 0.2:
                bot.forward(50)
            else:
                bot.stop()
        else:
            bot.stop()
        
    except:
        break
    
bot.stop()
cam.release()
```

# SerBot Example2 (PyQt + preview)
```python
import sys
import cv2
from threading import Thread

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import QCoreApplication

from pop import Pilot 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        cam_cmd = lambda cam_with=640, cam_height=480, win_with=640, win_height=480, rate=60, flip=0 : ('nvarguscamerasrc ! '
                    'video/x-raw(memory:NVMM), '
                    'width={0}, height={1}, '
                    'format=NV12, framerate={2}/1 ! '
                    'nvvidconv flip-method={3} ! '
                    'video/x-raw, width={4}, height={5}, '
                    'format=BGRx ! '
                    'videoconvert ! appsink').format(cam_with, cam_height, rate, flip, win_with, win_height)

        self.cam = cv2.VideoCapture(cam_cmd(), cv2.CAP_GSTREAMER)
        self.bot = Pilot.SerBot() 

        self.of = Pilot.Object_Follow2(self.cam, 640, 480)
        self.of.load_model()
        
        self.frame = QLabel(self)
        self.frame.resize(1280, 720)

        self.__is_run = True
        self.thread = Thread(target=self.__onObjectFollow2)
        self.thread.daemon = True
        self.thread.start()

        self.pbExit = QPushButton('Exit', self)
        self.pbExit.resize(120, 60)
        self.pbExit.setFont(QFont('', 50))
        self.pbExit.clicked.connect(self.onExit)
    
    def onExit(self):
        self.__is_run = False
        self.thread.join()
        self.cam.release()
        
        self.bot.stop()

        QCoreApplication.instance().quit()


    def __onObjectFollow2(self):
        while self.__is_run:
            h, image = self.of.detect(index='person')
        
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
            h,w,c = image.shape
            pixmap = QPixmap.fromImage(QImage(image.data, w, h, w * c, QImage.Format_RGB888))
            self.frame.setPixmap(pixmap)
        
            if h is not None: 
                steer = h['x'] * 4 
                if steer > 1:
                    steer = 1
                elif steer < -1:
                    steer = -1
                
                self.bot.steering = steer

                if h['size_rate'] < 0.2:
                    self.bot.forward(50)
                else:
                    self.bot.stop()
            else:
                self.bot.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())
```
