# -*- coding:utf-8 -*-
#QProgressBar控件
'''
setValue  setMinimum和setMaximum    0 - 100
'''
from PySide2.QtWidgets import QWidget,QProgressBar,QApplication,QPushButton
from PySide2.QtCore import QBasicTimer
import sys
class ProgressBar(QWidget):
    def __init__(self,parent=None):
        super(ProgressBar, self).__init__(parent)
        self.initUI()
    def initUI(self):
        self.pbar=QProgressBar(self)
        self.pbar.setGeometry(40,40,200,25)

        self.btn=QPushButton('开始',self)
        self.btn.move(40,80)
        self.btn.clicked.connect(self.doAction)

        self.timer=QBasicTimer()
        self.value=0
        self.setGeometry(300,300,280,170)
        self.setWindowTitle('QProgressBar控件')
        self.show()
    def timerEvent(self, e):    #递归？
        if self.value>=100:
            self.timer.stop()
            self.btn.setText('完成')
            return
        self.value=self.value+1
        self.pbar.setValue(self.value)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('开始')
        else:
            self.timer.start(100,self)
            self.btn.setText('停止')

if __name__=='__main__':
    app=QApplication(sys.argv)
    Pg=ProgressBar()
    sys.exit(app.exec_())