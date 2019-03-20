# -*- coding:utf-8 -*-
import sys
import maya.cmds as cmds
from PySide2 import QtWidgets
from PySide2 import QtCore, QtGui

class PB(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(PB, self).__init__(parent)
        self.setWindowTitle('PlayBlast')
        self.resize(400,450)
        self.mainlaoyout=QtWidgets.QGridLayout(self)

        self.label1=QtWidgets.QLabel(u'选择文件夹')
        self.label2=QtWidgets.QLabel(u'选择输出格式')
        self.label3=QtWidgets.QLabel(u'选择保存路径')


        self.openFileLineEdit=QtWidgets.QLineEdit()
        self.saveFileLineEdit=QtWidgets.QLineEdit()

        self.formatCombox=QtWidgets.QComboBox()
        self.formatCombox.setFixedWidth(180)
        self.formatCombox.addItems(['qt','avi','image'])

        self.button1=QtWidgets.QPushButton(u'打开')
        self.button1.setFixedSize(100,20)
        self.button1.clicked.connect(self.openFile)
        self.button2=QtWidgets.QPushButton(u'创建摄像机')
        self.button2.setFixedSize(150,20)
        self.button2.clicked.connect(self.createCamera)
        self.button3=QtWidgets.QPushButton(u'K帧')
        self.button3.setFixedSize(100,20)
        self.button3.clicked.connect(self.K_Frame)
        self.button4=QtWidgets.QPushButton(u'选择')
        self.button4.setFixedSize(100,20)
        self.button4.clicked.connect(self.ChoosePath)
        self.button5=QtWidgets.QPushButton(u'拍屏')
        self.button5.setFixedSize(150,20)
        self.button5.clicked.connect(self.playBlase)
        self.button6=QtWidgets.QPushButton(u'关闭')
        self.button6.setFixedSize(100,20)
        self.button6.clicked.connect(self.Close)
        
        self.mainlaoyout.addWidget(self.label1,0,0)
        self.mainlaoyout.addWidget(self.openFileLineEdit,0,1)
        self.mainlaoyout.addWidget(self.button1,0,2)
        self.mainlaoyout.addWidget(self.button2,1,1)
        self.mainlaoyout.addWidget(self.button3,1,2)
        self.mainlaoyout.addWidget(self.label2,2,0)
        self.mainlaoyout.addWidget(self.formatCombox,2,1)
        self.mainlaoyout.addWidget(self.label3,3,0)
        self.mainlaoyout.addWidget(self.saveFileLineEdit,3,1)
        self.mainlaoyout.addWidget(self.button4,3,2)
        self.mainlaoyout.addWidget(self.button5,4,1)
        self.mainlaoyout.addWidget(self.button6,4,2)

            

        
    def openFile(self):
        openPath=QtWidgets.QFileDialog.getOpenFileName(self,'Open','C:\Users\Admin\Documents\maya','*.*;;*.py;;*.mel;;*.ma;;*.mb')
        self.openFileLineEdit.setText(openPath[0])
        cmds.file(openPath[0],open=True,f=True)
    def createCamera(self):
        global CameraName
        CameraAttribute=cmds.camera()
        CameraName=CameraAttribute[0]
    def K_Frame(self):
        #K帧前，选择相机
        cmds.select(CameraName,r=True)
        global i
        i=1
        #移动相机的变换中心到网格中心
        cmds.move(0,0,0,CameraName+'.scalePivot',CameraName+'.rotatePivot',rpr=True)
        #移动时间滑块同时变换相机位置
        while i<=10:
            cmds.currentTime(5*i)
            i=i+1
            #每移动一次时间滑块，让相机沿Y旋转36°，旋转10次
            cmds.rotate(0,'36deg',0,r=True,os=True,fo=False,)
            #K帧
            cmds.setKeyframe()
    def ChoosePath(self):  #确定输出路径
        global nameAndPath
        nameAndPath=QtWidgets.QFileDialog.getSaveFileName(self,'Choose','C:\Users\Admin\Documents\maya','*.*;;*.avi;;*.mov;;*.image')
        self.saveFileLineEdit.setText(nameAndPath[0])
    def playBlase(self):
        #拍屏 进入创建的摄像机视角
        cmds.lookThru(CameraName)
        #获得下拉列表当前的文本内容(foramt)
        ComboxText=self.formatCombox.currentText()
        #存储路径与文件名称 nameAndPath
        #拍屏
        cmds.playblast(format=ComboxText,filename=nameAndPath[0])
    def Close(self):
        self.close()

ex = PB()
ex.show()
