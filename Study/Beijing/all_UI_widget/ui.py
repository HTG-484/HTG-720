#!/usr/bin/env python
# -*- coding:utf-8 -*-

# import sys
# import socket
# from PyQt4 import QtGui,QtCore
#
# class Icon(QtGui.QWidget):
#     def __init__(self,parent = None):
#         super(Icon, self).__init__(parent)
#         self.resize(250,150)
#         # self.setGeometry(300,300,250,150)
#         self.setWindowTitle('Icon')
#         pix = QtGui.QIcon('F:\Screenshot1.ico')
#         self.setWindowIcon(pix)
#         tips = 'This is a <b>QWidget</b> widget'
#         self.setToolTip(tips)
#         Font_type = QtGui.QFont('OldEnglish', 10)
#         QtGui.QToolTip.setFont(Font_type)
#         quit = QtGui.QPushButton('close',self)
#         quit.setGeometry(10,10,64,35)
#         quit.clicked.connect(self.close)
#
#     def closeEvent(self, event):
#         reply = QtGui.QMessageBox.question(self,'Message','Are you sure to quit?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
#         if reply == QtGui.QMessageBox.Yes:
#             event.accept()
#         else:
#             event.ignore()
#
#     def keyPressEvent(self, event):
#         if event.key() == QtCore.Qt.Key_Escape:
#             self.close()
#
    # def center(self):
    #     screen = QtGui.QDesktopWidget().screenGeometry()
    #     size = self.geometry()
    #     self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)
#
#
# if __name__ == '__main__':
#     app = QtGui.QApplication(sys.argv)
#     icon = Icon()
#     icon.show()
#     app.exec_()



import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QColor

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.initUI()
        self.resize(610, 550)
        self.setWindowTitle('Edit')
        self.setWindowIcon(QtGui.QIcon('picture\edit1.ico'))
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Plastique'))
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('windowsXp'))
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Macintosh'))
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('GTK'))
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('CDE'))
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('windows'))
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Motif'))

    def initUI(self):


        self.tabelDialog = TabDialog()
        self.textEdit = OneTabel()
        self.setCentralWidget(self.tabelDialog)


        openFile = QtGui.QAction(QtGui.QIcon('picture\open.ico'),'Open',self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open file')
        exit = QtGui.QAction(QtGui.QIcon('picture\exit.ico'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')

        exit.triggered.connect(self.close)
        openFile.triggered.connect(self.OpenFileDailog)
        # self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.statusBar()

        menubar = self.menuBar()
        Open = menubar.addMenu('&Open')
        Exit = menubar.addMenu('&Exit')
        Open.addAction(openFile)
        Exit.addAction(exit)

        openToolbar = self.addToolBar('Open')
        exitToolbar = self.addToolBar('Exit')
        exitToolbar.addAction(exit)
        openToolbar.addAction(openFile)

    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


    def centerWidget(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


    def OpenFileDailog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,'Open file','/home')
        fname = open(filename)
        data = fname.read()
        self.textEdit.textEdit.setText(str(data))


class TabDialog(QtGui.QDialog):
    def __init__(self,parent = None):
        super(TabDialog, self).__init__(parent)
        tabWidget = QtGui.QTabWidget()

        tabWidget.addTab(OneTabel(),"Edit")
        tabWidget.addTab(TwoTabel(),"Control")
        tabWidget.addTab(ThreeTabel(),"Itemshift")
        tabWidget.addTab(FourTabel(),'ColorPainter')
        tabWidget.addTab(FiveTabel(),"BurningWidget")

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)



class OneTabel(QtGui.QWidget):
    def __init__(self):
        super(OneTabel, self).__init__()
        #self.resize(500,300)
        # color = QtGui.QColor(170,255,127)
        # self.setStyleSheet("QWidget {background-color: %s }" % color.name())
        self.initUI()

    def initUI(self):

        button1 = QtGui.QPushButton(u'消息框',self)
        button2 = QtGui.QPushButton(u'输入框',self)
        button3 = QtGui.QPushButton(u'颜色框',self)
        button4 = QtGui.QPushButton(u'字体对话框',self)
        self.textEdit = QtGui.QTextEdit()

        self.hlay = QtGui.QHBoxLayout()
        self.hlay.addWidget(button1)
        self.hlay.addWidget(button2)
        self.hlay.addWidget(button3)
        self.hlay.addWidget(button4)

        self.vlay = QtGui.QVBoxLayout()
        self.vlay.addWidget(self.textEdit)
        self.vlay.addLayout(self.hlay)
        self.setLayout(self.vlay)
        button1.clicked.connect(self.Messagebox)
        button2.clicked.connect(self.Inputdialog)
        button3.clicked.connect(self.Colordialog)
        button4.clicked.connect(self.Fontdialog)

    def Messagebox(self):
        message = QtGui.QMessageBox()
        reply = message.question(self,u'你好啊！',u'很高兴认识你！',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.textEdit.setText(u'hello,pyqt')
        # else:
        #     color = QtGui.QColorDialog.getColor(QtCore.Qt.green,self)
        #     if color.isValid():
        #         self.textEdit.setPalette(QtGui.QPalette(color))
        #         self.textEdit.setAutoFillBackground(True)


    def Inputdialog(self):
        text,ok = QtGui.QInputDialog.getText(self,'In put Dialog','Enter your name:')
        if ok:
            self.textEdit.setText(str(text))

    def Colordialog(self):
        col = QtGui.QColorDialog.getColor()
        if col:
            self.setStyleSheet("QWidget { background-color: %s }" % col.name())

    def Fontdialog(self):
        font,ok = QtGui.QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

class TwoTabel(QtGui.QWidget):
    def __init__(self,parent = None):
        super(TwoTabel, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.checkbox = QtGui.QCheckBox('show image',self)
        self.checkbox.toggle()
        self.text = QtGui.QLineEdit()
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.slider_value = QtGui.QLabel()
        self.label = QtGui.QLabel()
        self.progressBar = QtGui.QProgressBar()
        self.startButton = QtGui.QPushButton('Start',self)
        self.resetButton = QtGui.QPushButton('Reset',self)

        self.calender = QtGui.QCalendarWidget()
        self.cal_label = QtGui.QLabel()
        self.pix_label = QtGui.QLabel()
        self.pix_label.setPixmap(QtGui.QPixmap('picture/smile.ico'))

        self.calender.setGridVisible(True)
        self.cal_label.setText(str(self.calender.selectedDate().toPyDate()))

        self.time = QtCore.QBasicTimer()
        self.step = 0

        self.label.setPixmap(QtGui.QPixmap('picture/mute.ico'))
        self.HLay = QtGui.QHBoxLayout()
        self.HLay.addWidget(self.checkbox)
        self.HLay.addWidget(self.text)

        self.HLay1 = QtGui.QHBoxLayout()
        self.HLay1.addWidget(self.label)
        self.HLay1.addWidget(self.slider)
        self.HLay1.addWidget(self.slider_value)

        self.HLay2 = QtGui.QHBoxLayout()
        self.HLay2.addWidget(self.startButton)
        self.HLay2.addWidget(self.progressBar)
        self.HLay2.addWidget(self.resetButton)

        # self.splitter = QtGui.QSplitter()
        # self.splitter.addWidget()

        self.VLay = QtGui.QVBoxLayout()
        self.VLay.addLayout(self.HLay)
        self.VLay.addLayout(self.HLay1)
        self.VLay.addLayout(self.HLay2)
        self.VLay.addWidget(self.calender)
        self.VLay.addWidget(self.cal_label)
        self.VLay.addWidget(self.pix_label)
        #self.VLay.addSpacing(100)

        self.setLayout(self.VLay)
        self.calender.selectionChanged.connect(self.showData)
        self.startButton.clicked.connect(self.ProgressBarDoAction)
        self.resetButton.clicked.connect(self.resetprogressBar)
        self.checkbox.stateChanged.connect(self.changeText)
        self.slider.valueChanged.connect(self.valueChange)
#chckebox按钮
    def changeText(self):
        if self.checkbox.isChecked():
            self.text.setText(u'已选')
        else:
            self.text.setText(u'未选')
#改变图标的function
    def valueChange(self):
        sliderValue = self.slider.value()
        self.slider_value.setText(str(sliderValue))
        if sliderValue == 0:
            self.label.setPixmap(QtGui.QPixmap('picture/mute.ico'))
        elif sliderValue >0 and sliderValue<=30:
            self.label.setPixmap(QtGui.QPixmap('picture/sound.ico'))
#第一种进度条
    def timerEvent(self, event):

        if self.step>=100:
            self.time.stop()
            return
        self.step = self.step +1
        self.progressBar.setValue(self.step)
    def ProgressBarDoAction(self):
        if self.time.isActive():
            self.time.stop()
            self.startButton.setText('Start')
        else:
            self.time.start(10,self)
            self.startButton.setText('Stop')
#第二种进度条
    # def ProgressBarDoAction(self):
    #     number = 100                                #可以是一个长度
    #     self.progressBar.setMinimum(0)
    #     self.progressBar.setMaximum(number)
    #     for i in range(number):
    #         self.progressBar.setValue(i + 1)
    #         QtCore.QThread.msleep(10)
    #     else:
    #         pass

    def resetprogressBar(self):
        self.progressBar.reset()
#显示信息的function
    def showData(self):
        data = self.calender.selectedDate()
        self.cal_label.setText(str(data.toPyDate()))

class ThreeTabel(QtGui.QWidget):
    def __init__(self,parent = None):
        super(ThreeTabel, self).__init__(parent)
        self.initUI()
    def initUI(self):
        self.Linedit = QtGui.QLineEdit()
        self.button = QtGui.QPushButton('Smile',self)
        self.button.setIcon(QtGui.QIcon('picture/smile'))
        self.rightlistwidget = ListWidget()
        self.rightlistwidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)    #设置选择模式按住ctrl多选
        self.rightlistwidget.setDragEnabled(True)
        for i in range(1,10):
            self.rightlistwidget.addItem('Item'+str(i) )
        # self.rightlistwidget.addItem('aaa')
        # self.rightlistwidget.addItem('bbb')
        self.rightButton = QtGui.QPushButton(u'右移>>',self)
        self.rightButton.setEnabled(False)
        self.leftButton = QtGui.QPushButton(u'左移<<',self)
        self.leftButton.setEnabled(False)
        self.leftlisdtwidget = QtGui.QListWidget()
        self.leftlisdtwidget.addItem('a')

        self.upLay = QtGui.QHBoxLayout()
        self.upLay.addWidget(self.Linedit)
        self.upLay.addWidget(self.button)

        self.btnHlay = QtGui.QVBoxLayout()
        self.btnHlay.addSpacing(100)
        self.btnHlay.addWidget(self.rightButton)
        self.btnHlay.addWidget(self.leftButton)
        self.btnHlay.addSpacing(100)

        # self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        # self.splitter.addWidget(self.rightlistwidget)
        # self.splitter.addWidget(self.leftlisdtwidget)

        self.downLay = QtGui.QHBoxLayout()
        self.downLay.addWidget(self.rightlistwidget)
        self.downLay.addLayout(self.btnHlay)
        self.downLay.addWidget(self.leftlisdtwidget)

        self.Vlay = QtGui.QVBoxLayout()
        self.Vlay.addLayout(self.upLay)
        self.Vlay.addLayout(self.downLay)
        self.setLayout(self.Vlay)

        self.rightButton.clicked.connect(self.Right_shift)
        self.leftButton.clicked.connect(self.Left_shift)
        self.rightlistwidget.itemDoubleClicked.connect(self.showmessage)
        self.rightlistwidget.itemPressed.connect(self.rightbuttonActive)
        self.leftlisdtwidget.itemPressed.connect(self.leftbuttonActive)


    def Right_shift(self):
        # item = self.rightlistwidget.currentRow() #移除单行列的item
        # self.rightlistwidget.takeItem(item)

        item = self.rightlistwidget.selectedItems()
        for i in item:
            #self.rightlistwidget.takeItem(i)
            self.rightlistwidget.setItemHidden(i,True)
            #self.leftlisdtwidget.insertItem(i)
        self.leftlisdtwidget.addItem(self.rightlistwidget.currentItem().text())

    def Left_shift(self):
        item = self.leftlisdtwidget.selectedItems()
        for i in item:
            self.leftlisdtwidget.setItemHidden(i,True)
        self.rightlistwidget.addItem(self.leftlisdtwidget.currentItem().text())

    def showmessage(self):
        message = QtGui.QMessageBox()
        message.information(self,u'信息',u'这是Item的所有信息')

    def rightbuttonActive(self):
        self.rightButton.setEnabled(True)

    def leftbuttonActive(self):
        self.leftButton.setEnabled(True)



#未完成，待解决
class ListWidget(QtGui.QListWidget):
    def __init__(self,parent = None):
        super(ListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        #self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData().hasImage()
        if data:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self,event):
        event.accept()
        #self.dragMoveEvent(event)

    def dropEvent(self, event):
        data = event.mimeData()
        event.accept()

    def deleteItem(self,item):

        self.takeItem(item)

        # urls = data.urls()
        # self.information = []
        # if (urls and urls[0].scheme() == 'file'):
        #     urls[0].setScheme("")
        #     for uu in urls:
        #         self.addItem(uu)



class FourTabel(QtGui.QWidget):
    def __init__(self,parent = None):
        super(FourTabel, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.text = u'\u041b\u0435\u0432 \u041d\u0438\u043a\u043e\u043b\u0430\
                  \u0435\u0432\u0438\u0447 \u0422\u043e\u043b\u0441\u0442\u043e\u0439: \n\
                  \u0410\u043d\u043d\u0430 \u041a\u0430\u0440\u0435\u043d\u0438\u043d\u0430'

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        # self.drawText(e, qp)
        # self.drawPoints(qp)
        # self.drawRectangles(qp)
        # self.doDrawing(qp)
        self.drawBrushes(qp)
        qp.end()

    def drawPoints(self, qp):

        qp.setPen(QtCore.Qt.red)
        size = self.size()

        for i in range(1000):
            x = random.randint(1, size.width()-1)
            y = random.randint(1, size.height()-1)
            qp.drawPoint(x, y)

    def drawText(self, event, qp):

        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def drawRectangles(self, qp):
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)

        qp.setBrush(QtGui.QColor(255, 0, 0, 80))
        qp.drawRect(10, 15, 90, 60)

        qp.setBrush(QtGui.QColor(255, 0, 0, 160))
        qp.drawRect(130, 15, 90, 60)

        qp.setBrush(QtGui.QColor(255, 0, 0, 255))
        qp.drawRect(250, 15, 90, 60)

        qp.setBrush(QtGui.QColor(10, 163, 2, 55))
        qp.drawRect(10, 105, 90, 60)

        qp.setBrush(QtGui.QColor(160, 100, 0, 255))
        qp.drawRect(130, 105, 90, 60)

        qp.setBrush(QtGui.QColor(60, 100, 60, 255))
        qp.drawRect(250, 105, 90, 60)

        qp.setBrush(QtGui.QColor(50, 50, 50, 255))
        qp.drawRect(10, 195, 90, 60)

        qp.setBrush(QtGui.QColor(50, 150, 50, 255))
        qp.drawRect(130, 195, 90, 60)

        qp.setBrush(QtGui.QColor(223, 135, 19, 255))
        qp.drawRect(250, 195, 90, 60)

    def doDrawing(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(20, 40, 250, 40)

        pen.setStyle(QtCore.Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(20, 80, 250, 80)

        pen.setStyle(QtCore.Qt.DashDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 120, 250, 120)

        pen.setStyle(QtCore.Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(20, 160, 250, 160)

        pen.setStyle(QtCore.Qt.DashDotDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 200, 250, 200)

        pen.setStyle(QtCore.Qt.CustomDashLine)
        pen.setDashPattern([1, 4, 5, 4])
        qp.setPen(pen)
        qp.drawLine(20, 240, 250, 240)

    def drawBrushes(self, qp):
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 15, 90, 60)

        brush.setStyle(QtCore.Qt.Dense1Pattern)
        qp.setBrush(brush)
        qp.drawRect(130, 15, 90, 60)

        brush.setStyle(QtCore.Qt.Dense2Pattern)
        qp.setBrush(brush)
        qp.drawRect(250, 15, 90, 60)

        brush.setStyle(QtCore.Qt.Dense3Pattern)
        qp.setBrush(brush)
        qp.drawRect(10, 105, 90, 60)

        brush.setStyle(QtCore.Qt.DiagCrossPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 105, 90, 60)

        brush.setStyle(QtCore.Qt.Dense5Pattern)
        qp.setBrush(brush)
        qp.drawRect(130, 105, 90, 60)

        brush.setStyle(QtCore.Qt.Dense6Pattern)
        qp.setBrush(brush)
        qp.drawRect(250, 105, 90, 60)

        brush.setStyle(QtCore.Qt.HorPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 195, 90, 60)

        brush.setStyle(QtCore.Qt.VerPattern)
        qp.setBrush(brush)
        qp.drawRect(130, 195, 90, 60)

        brush.setStyle(QtCore.Qt.BDiagPattern)
        qp.setBrush(brush)
        qp.drawRect(250, 195, 90, 60)


class FiveTabel(QtGui.QWidget):

    def __init__(self):
        super(FiveTabel, self).__init__()

        self.initUI()

    def initUI(self):

        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider.setFocusPolicy(QtCore.Qt.NoFocus)
        slider.setRange(1, 750)
        slider.setValue(75)
        slider.setGeometry(30, 40, 500, 500)

        self.wid = BurningWidget()

        slider.valueChanged.connect(self.changeValue)
        # self.connect(slider, QtCore.SIGNAL('valueChanged(int)'),
        #     self.changeValue)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.wid)
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Burning')

    def changeValue(self, value):

        self.wid.emit(QtCore.SIGNAL("updateBurningWidget(int)"), value)
        self.wid.repaint()

class BurningWidget(QtGui.QWidget):
    def __init__(self,parent = None):
        super(BurningWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.setMinimumSize(1, 30)
        self.value = 75
        self.num = [75, 150, 225, 300, 375, 450, 525, 600, 675]

        self.connect(self, QtCore.SIGNAL("updateBurningWidget(int)"),
            self.setValue)

    def setValue(self, value):

        self.value = value


    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()


    def drawWidget(self, qp):

        font = QtGui.QFont('Serif', 7, QtGui.QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        step = int(round(w / 10.0))


        till = int(((w / 750.0) * self.value))
        full = int(((w / 750.0) * 700))

        if self.value >= 700:
            qp.setPen(QtGui.QColor(255, 255, 255))
            qp.setBrush(QtGui.QColor(255, 255, 184))
            qp.drawRect(0, 0, full, h)
            qp.setPen(QtGui.QColor(255, 175, 175))
            qp.setBrush(QtGui.QColor(255, 175, 175))
            qp.drawRect(full, 0, till-full, h)
        else:
            qp.setPen(QtGui.QColor(255, 255, 255))
            qp.setBrush(QtGui.QColor(255, 255, 184))
            qp.drawRect(0, 0, till, h)

        pen = QtGui.QPen(QtGui.QColor(20, 20, 20), 1,
            QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)

        j = 0

        for i in range(step, 10*step, step):

            qp.drawLine(i, 0, i, 5)
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))
            qp.drawText(i-fw/2, h/2, str(self.num[j]))
            j = j + 1



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())



# from PyQt4.QtGui import QColor, QWidget
# from PyQt4 import QtGui
# class mywindow(QWidget):
#     def __init__(self):
#         super(mywindow, self).__init__()
#         if __name__ == '__main__':
#             import sys
#             app = QtGui.QApplication(sys.argv)
#             w = mywindow()
#             grid = QtGui.QGridLayout()
#             i = j = 0
#             row = 15
#             print(len(QColor.colorNames()))
#             for name in QColor.colorNames():
#                 label = QtGui.QLabel()
#                 label.setText(name)
# #通过亮度决定文字颜色
#                 if QColor(name).getHsv()[2] > 200:
#                         label.setStyleSheet("QLabel{background-color: " + name + ";font: 16px;color: black;}")
#                 else:
#                     label.setStyleSheet("QLabel{background-color: " + name + ";font: 16px;color: white;}")
#                     grid.addWidget(label, i % row, j)
#                     temp = i % row
#                     i += 1
#                     if i % row < temp % row:
#                         j += 1
#             w.setLayout(grid)
#             w.show()
#             sys.exit(app.exec_())


# import sys
# from PyQt4 import QtGui, QtCore
#
# class Example(QtGui.QWidget):
#
#     def __init__(self):
#         super(Example, self).__init__()
#         self.initUI()
#
#     def initUI(self):
#
#         self.connect(self, QtCore.SIGNAL('closeEmitApp()'),
#             QtCore.SLOT('close()'))
#
#         self.setWindowTitle('emit')
#         self.resize(250, 150)
#
#     def mousePressEvent(self, event):                 #定义信号
#         self.emit(QtCore.SIGNAL('closeEmitApp()'))
#
# app = QtGui.QApplication(sys.argv)
# ex = Example()
# ex.show()
# sys.exit(app.exec_())




# import sys
# from PyQt4 import QtGui
# from PyQt4 import QtCore
#
#
# class Example(QtGui.QWidget):
#
#     def __init__(self):
#         super(Example, self).__init__()
#
#         self.initUI()
#
#     def initUI(self):
#
#         self.color = QtGui.QColor(0, 0, 0)
#
#         self.red = QtGui.QPushButton('Red', self)
#         self.red.setCheckable(True)
#         self.red.move(10, 10)
#
#         self.connect(self.red, QtCore.SIGNAL('clicked()'), self.setColor)
#
#         self.green = QtGui.QPushButton('Green', self)
#         self.green.setCheckable(True)
#         self.green.move(10, 60)
#
#         self.connect(self.green, QtCore.SIGNAL('clicked()'), self.setColor)
#
#         self.blue = QtGui.QPushButton('Blue', self)
#         self.blue.setCheckable(True)
#         self.blue.move(10, 110)
#
#         self.connect(self.blue, QtCore.SIGNAL('clicked()'), self.setColor)
#
#         self.square = QtGui.QWidget(self)
#         self.square.setGeometry(150, 20, 100, 100)
#         self.square.setStyleSheet("QWidget { background-color: %s }" %
#             self.color.name())
#
#         self.setWindowTitle('ToggleButton')
#         self.setGeometry(300, 300, 280, 170)
#
#
#     def setColor(self):
#
#         source = self.sender()
#
#         if source.text() == "Red":
#             if self.red.isChecked():
#                 self.color.setRed(255)
#             else: self.color.setRed(0)
#
#         elif source.text() == "Green":
#             if self.green.isChecked():
#                 self.color.setGreen(255)
#             else: self.color.setGreen(0)
#
#         else:
#             if self.blue.isChecked():
#                 self.color.setBlue(255)
#             else: self.color.setBlue(0)
#
#         self.square.setStyleSheet("QWidget { background-color: %s }" %
#             self.color.name())
#
#
#
# if __name__ == '__main__':
#
#     app = QtGui.QApplication(sys.argv)
#     ex = Example()
#     ex.show()
#     app.exec_()