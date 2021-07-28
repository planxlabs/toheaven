# PyQt5 (second_omniwheel.py)
```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QCheckBox, QLabel, QLineEdit, QGroupBox

from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
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

        onClickedHandler = [self.OnClieckedStart, self.onClickedStop, self.onClickedExit]
        pbTitle = ['Start', 'Stop', 'Exit']

        for i in range(len(pbTitle)):
            pb = QPushButton(pbTitle[i], self)
            pb.move(210 + i * 320, 480)
            pb.resize(200, 100)
            pb.clicked.connect(onClickedHandler[i])
            pb.setFont(QFont('Arial', 50))


    def OnClieckedStart(self):
        if self.cbForward.isChecked(): 
            print("forward")
        else:
            print("backward")
    
    def onClickedStop(self):
        print("stop")
    
    def onClickedExit(self):
        print("exit")
        QCoreApplication.instance().quit()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
```
