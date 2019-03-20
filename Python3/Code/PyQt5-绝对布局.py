#绝对布局
import sys
from PySide2.QtWidgets import QWidget,QLabel,QApplication

class Absolutelayout(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        Label1=QLabel('姓名',self)
        Label1.move(15,10)

        Label2=QLabel('年龄',self)
        Label2.move(35,40)

        Label3=QLabel('所在城市',self)
        Label3.move(55,70)

        self.setGeometry(300,300,300,200)
        self.setWindowTitle('绝对布局')
        self.show()
if __name__=='__main__':
    app=QApplication(sys.argv)
    al=Absolutelayout()
    sys.exit(app.exec_())