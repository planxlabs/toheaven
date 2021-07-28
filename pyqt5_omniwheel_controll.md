# Bug Fix(app exit issus) of OmniWheel (pop > CAN.py > class OmniWheel) 
```python
class OmniWheel:
    def __init__(self):
        #super().__init__()
        ...
        self._is_read = False
    
    def __del__(self):
        #super().__del__()
        ...
        
    def _readSensor(self):
        #while True:
        while self._is_read:
            ...
    
    def readStart(self):
        if not hasattr(__main__, ...
            self._is_read = True
            ...
    
    def readStop(self):
        if hasattr(self, 'thread'):
            self._is_read = False
            ...
```

# PyQt5 (second_omniwheel.py)
```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QCheckBox, QLabel, QLineEdit, QGroupBox
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication

from pop.CAN import OmniWheel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.omni = OmniWheel()

        #self.showFullScreen()
        self.move(0,0)
        self.resize(1280, 720)
        self.setWindowTitle("OmniWheel Control")
        self.init()

    def init(self):
        gb1 = QGroupBox(self)
        gb1.move(80, 50)
        gb1.resize(1120, 400)

        self.cbForward = QCheckBox(' Forward', self)
        self.cbForward.move(100, 80)
        self.cbForward.setFont(QFont('Arial', 80))
        self.setStyleSheet("QCheckBox::indicator {width: 50px; height: 50px;}")

        self.motorEdit = []
        step = 80
        for i in range(3):        
            motorLabel = QLabel("Motor%d"%(i + 1), self)
            motorLabel.move(100, 200 + (i * step))
            motorLabel.setFont(QFont('Arial', 90))

            self.motorEdit.append(QLineEdit(self))
            self.motorEdit[i].move(100 + 180, 200 + (i * step))
            self.motorEdit[i].resize(900, 70)
            self.motorEdit[i].setFont(QFont('Arial', 80))

        gb2 = QGroupBox(self)
        gb2.move(80, 460)
        gb2.resize(1120, 130)

        self.pbControl = [QPushButton('Start', self), QPushButton('Stop', self), QPushButton('Exit', self)]
        onClickedHandler = [self.OnClieckedStart, self.onClickedStop, self.onClickedExit]

        for i, pb in enumerate(self.pbControl):
            pb.move(210 + i * 320, 480)
            pb.resize(200, 100)
            pb.clicked.connect(onClickedHandler[i])
            pb.setFont(QFont('Arial', 50))

        self.pbControl[1].setEnabled(False)

    def OnClieckedStart(self):
        wheel = []
        for e in self.motorEdit:
            try:
                wheel.append(int(e.text()))
            except ValueError:
                msg = QMessageBox(3, "Error", "Motor PWM Value Error", QMessageBox.Ok)
                msg.setFont(QFont('Arial',50))
                msg.exec()
                return

        if self.cbForward.isChecked():
            self.omni.forward(wheel) 
        else:
            self.omni.backward(wheel)
        
        self.pbControl[0].setEnabled(False)
        self.pbControl[1].setEnabled(True)
        
                        
    def onClickedStop(self):
        self.omni.stop()
    
        self.pbControl[0].setEnabled(True)
        self.pbControl[1].setEnabled(False)

    def onClickedExit(self):
        print("exit")
        QCoreApplication.instance().quit()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
```
