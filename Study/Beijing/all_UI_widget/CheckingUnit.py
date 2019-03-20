#-*- coding: utf-8 -*-

#
# import sys
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox, QLabel, QPushButton, QRadioButton, QVBoxLayout, QWidget)
#
# list_food = ["Pizza", "Taco", "Burrito"]
#
# class Window(QWidget):
#     def __init__(self):
#         super(Window, self).__init__()
#
#         self.setWindowTitle("PyQt5 Group Box")
#         self.resize(400, 300)
#
#         self.groupBox = QGroupBox("Best Food")
#
#         # Checkbox layout
#         self.vbox = QVBoxLayout()
#
#         for i in range(len(list_food)):
#             self.cbx = QCheckBox(list_food[i])
#             self.vbox.addWidget(self.cbx)
#             self.cbx.stateChanged.connect(self.change_food)
#         #cbx1.setChecked(True)              #问题一：如何默认选定列中的第一项？
#         self.lbl_result = QLabel("food now is/are: " + "")
#         self.vbox.addWidget(self.lbl_result)
#
#         self.groupBox.setLayout(self.vbox)
#
#         # vertical box layout
#         self.vlayout = QVBoxLayout()
#         self.vlayout.addWidget(self.groupBox)
#         self.vlayout.addStretch()
#         self.setLayout(self.vlayout)
#
#     def change_food(self):
#         self.lbl_result.setText("you changed food to: " + "")    #问题二，如何读取选定的CheckBox？
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     clock = Window()
#     clock.show()
#     sys.exit(app.exec_())




import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit, QDockWidget, QListWidget
from PySide2.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.items = ['呵呵', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff','g', 'h', 'i', 'j', 'k', 'l', 'm'
                 ,'m','n','o','p','q','r','s','t']
        self.init()
        self.addDock()


    def init(self):
        self.text = QListWidget()
        #self.text.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.text)

        self.setGeometry(200, 200, 800, 400)
        self.setWindowTitle('QDockWidget示例')
        self.show()
        pass

    def onDockListIndexChanged(self, index):
        item = self.items[index]
        self.text.addItem(item)
        pass

    def addDock(self):
        dock1 = QDockWidget('DockWidget')
        dock1.setFeatures(QDockWidget.DockWidgetFloatable)
        dock1.setAllowedAreas(Qt.LeftDockWidgetArea)
        listwidget = QListWidget()

        listwidget.addItems(self.items)
        listwidget.currentRowChanged.connect(self.onDockListIndexChanged)
        dock1.setWidget(listwidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


# 入口
if __name__ == '__main__':
    main()




