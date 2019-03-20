import sys
from PySide2.QtWidgets import *
class CenterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.resize(600,500)
        self.setWindowTitle('窗口居中')
        self.center()
        self.show()
    def center(self):
        desktop=app.desktop()
        self.move((desktop.width()-self.width())/4,(desktop.height()-self.height())/2) #双屏
app=QApplication(sys.argv)
cw=CenterWindow()
sys.exit(app.exec())
