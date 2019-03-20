import sys
from PySide2.QtWidgets import QApplication,QToolTip,QPushButton,QWidget
from PySide2.QtGui import QFont
app=QApplication(sys.argv)
w=QWidget()
w.setGeometry(300,300,300,220)
w.setWindowTitle('提示框')
QToolTip.setFont(QFont('SansSerif',20))
w.setToolTip('这是一个窗口\n设计者：HTG')
button=QPushButton('Button',w)
button.setToolTip('这是一个按钮\n设计者：HTG')
button.resize(button.sizeHint())
button.move(50,50)
w.show()
sys.exit(app.exec_())