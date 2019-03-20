import sys
from PySide2.QtWidgets import QApplication,QWidget,QPushButton
from PySide2.QtCore import QCoreApplication
app=QApplication(sys.argv)
w=QWidget()
w.setGeometry(300,300,300,220)
w.setWindowTitle('关闭窗口')
button=QPushButton('关闭窗口',w)
button.clicked.connect(QCoreApplication.instance().quit)
button.move(50,50)
w.show()
sys.exit(app.exec_())