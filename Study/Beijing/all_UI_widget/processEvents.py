# -*- coding:utf-8 -*-
# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
import time

class Test(QDialog):
    def __init__(self,parent=None):
        super(Test,self).__init__(parent)
        self.listFile=QListWidget()
        self.btnStart=QPushButton('Start')
        layout=QGridLayout(self)
        layout.addWidget(self.listFile,0,0,1,2)
        layout.addWidget(self.btnStart,1,1)
        self.connect(self.btnStart,SIGNAL('clicked()'),self.slotAdd)
    def slotAdd(self):
        for n in range(10):
            str_n='File index {0}'.format(n)
            self.listFile.addItem(str_n)
            QApplication.processEvents()
            time.sleep(1)
app=QApplication(sys.argv)
dlg=Test()
dlg.show()
sys.exit(app.exec_())
