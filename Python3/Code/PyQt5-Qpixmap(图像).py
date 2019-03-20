# -*- coding:utf-8 -*-
#QPixmap 控件

from PySide2.QtWidgets import QWidget,QHBoxLayout,QLabel,QApplication
from PySide2.QtGui import QPixmap
import sys
class Pixmap(QWidget):
    def __init__(self,parent=None):
        super(Pixmap, self).__init__(parent)
        self.initUI()
    def initUI(self):
        hbox=QHBoxLayout(self)

        pixmap=QPixmap('魔鬼')
        lbl=QLabel(self)
        lbl.setPixmap(pixmap)
        hbox.addWidget(lbl)
        self.setLayout(hbox)
        self.move(300,200)
        self.setWindowTitle('显示图像')
        self.show()

if __name__=='__main__':
    app=QApplication(sys.argv)
    pi=Pixmap()
    sys.exit(app.exec_())