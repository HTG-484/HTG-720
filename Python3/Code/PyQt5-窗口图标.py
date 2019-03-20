import sys
from PySide2.QtWidgets import QApplication,QWidget
from PySide2.QtGui import QIcon
app=QApplication(sys.argv)
w=QWidget()
w.setGeometry(300,300,300,220)
w.setWindowTitle('窗口图标')
app.setWindowIcon(QIcon('python.jpg'))
w.show()
sys.exit(app.exec_())