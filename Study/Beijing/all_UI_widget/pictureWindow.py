#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
from PySide import QtGui, QtCore

PATH = ["G:\Beijing\Nuke\Library\\1.jpg","G:\Beijing\Nuke\Library\\5.jpg"]

class PictureWindow(QtGui.QMainWindow):
    def __init__(self,parent = None):
        super(PictureWindow, self).__init__(parent)
        #QtGui.QMainWindow.__init__(self)
        self.realmScroll = QtGui.QScrollArea(self)
        self.setCentralWidget(self.realmScroll)
        self.realmScroll.setWidgetResizable(True)

        labelsContainer = QtGui.QWidget()
        self.setWindowTitle("Picture Window")
        self.resize(400, 400)

        self.realmScroll.setWidget(labelsContainer)

        labelsLayout = QtGui.QVBoxLayout(labelsContainer)

        for i in PATH:
            image = QtGui.QPixmap(i).scaled(400, 200, QtCore.Qt.KeepAspectRatio)

            label = QtGui.QLabel()
            label.setPixmap(image)
            label.setScaledContents(True)
            labelsLayout.addWidget(label)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    test = PictureWindow()
    test.show()
    app.exec_()