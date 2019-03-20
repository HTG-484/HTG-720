# -*- coding:utf-8 -*-
#QSlide控件
'''
valueChanged     setMinimum和 setMaximum
'''
from PySide2.QtWidgets import QWidget,QSlider,QLabel,QApplication
from PySide2.QtCore import Qt
import sys
class Slider(QWidget):
    def __init__(self,parent=None):
        super(Slider, self).__init__(parent)
        self.initUI()
    def initUI(self):
        slider=QSlider(Qt.Horizontal,self)   #Horizontal水平滑块控件,Vertical垂直滑块控件
        slider.setMinimum(10)
        slider.setMaximum(500)
        slider.setGeometry(30,40,100,30)
        slider.valueChanged[int].connect(self.changeValue)

        self.label=QLabel(self)
        self.label.setGeometry(160,40,80,30)
        self.setGeometry(300,300,280,170)
        self.setWindowTitle('QSlider控件')
        self.show()
    def changeValue(self,value):
        self.label.setText(str(value))

if __name__=='__main__':
    app=QApplication(sys.argv)
    sl=Slider()
    sys.exit(app.exec_())