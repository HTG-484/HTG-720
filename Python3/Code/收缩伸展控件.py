# -*- coding:utf-8 -*-

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


class Spoiler(QtWidgets.QWidget):
    def __init__(self, parent=None, title='HaHaHaHaHaHa'):
        super(Spoiler, self).__init__(parent)
#if 此处可以跳过不看
        self.groupBox = QtWidgets.QGroupBox(self)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)

        self.pushButton3 = QtWidgets.QPushButton(self.groupBox)
        self.verticalLayout.addWidget(self.pushButton3)

        self.pushButton2 = QtWidgets.QPushButton(self.groupBox)
        self.verticalLayout.addWidget(self.pushButton2)

        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.verticalLayout.addWidget(self.label_2)

        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.verticalLayout.addWidget(self.pushButton)

        self.animationDuration = 300   #动画 持续？
        self.toggleAnimation = QtCore.QParallelAnimationGroup()  #动画？
        self.contentArea = QtWidgets.QScrollArea()  #滚动视图？
        self.headerLine = QtWidgets.QFrame()        #框架？
        self.toggleButton = QtWidgets.QToolButton() #快速访问按钮
        self.mainLayout = QtWidgets.QGridLayout()   #布局


        toggleButton = self.toggleButton
        toggleButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon) #设置按钮风格
        toggleButton.setArrowType(QtCore.Qt.RightArrow)
        toggleButton.setText(str(title))
        toggleButton.setCheckable(True)        #属性 可以被选中
        toggleButton.setChecked(False)          #值  未被选中

        # toggleButton = self.toggleButton
        # toggleButton.setText(str(title))
        # toggleButton.setCheckable(True)   #可以被选中
        # toggleButton.setChecked(False)    #不可被选中状态

        headerLine = self.headerLine
        headerLine.setFrameShape(QtWidgets.QFrame.HLine)
        headerLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        headerLine.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
#endif  以下开始为源代码

        self.contentArea.setStyleSheet(
            "QScrollArea { background-color: white; border: none; }")
        self.contentArea.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)
        # let the entire widget grow and shrink with its content
        toggleAnimation = self.toggleAnimation
        toggleAnimation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumHeight"))
        toggleAnimation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumHeight"))
        toggleAnimation.addAnimation(
            QtCore.QPropertyAnimation(self.contentArea, b"maximumHeight"))
        # don't waste space
        mainLayout = self.mainLayout
        mainLayout.setVerticalSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        row = 0
        mainLayout.addWidget(self.toggleButton, row, 0,
                             1, 1, QtCore.Qt.AlignLeft)
        mainLayout.addWidget(self.headerLine, row, 2, 1, 1)
        row += 1
        mainLayout.addWidget(self.contentArea, row, 0, 1, 3)
        self.setLayout(self.mainLayout)

        def start_animation(checked):
            arrow_type = QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow
            direction = QtCore.QAbstractAnimation.Forward if checked else QtCore.QAbstractAnimation.Backward
            toggleButton.setArrowType(arrow_type)
            self.toggleAnimation.setDirection(direction)
            self.toggleAnimation.start()

        self.toggleButton.clicked.connect(start_animation)

    def setContentLayout(self, contentLayout):
        # Not sure if this is equivalent to self.contentArea.destroy()
        self.contentArea.destroy()
        self.contentArea.setLayout(contentLayout)
        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()
        for i in range(self.toggleAnimation.animationCount()-1):
            spoilerAnimation = self.toggleAnimation.animationAt(i)
            spoilerAnimation.setDuration(self.animationDuration)
            spoilerAnimation.setStartValue(collapsedHeight)
            spoilerAnimation.setEndValue(collapsedHeight + contentHeight)
        contentAnimation = self.toggleAnimation.animationAt(
            self.toggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    ui = Spoiler()
    ui.setContentLayout(ui.verticalLayout)
    ui.show()

    sys.exit(app.exec_())