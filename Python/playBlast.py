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

        self.label1=QtWidgets.QLabel(u'ѡ���ļ���')
        self.label2=QtWidgets.QLabel(u'ѡ�������ʽ')
        self.label3=QtWidgets.QLabel(u'ѡ�񱣴�·��')


        self.openFileLineEdit=QtWidgets.QLineEdit()
        self.saveFileLineEdit=QtWidgets.QLineEdit()

        self.formatCombox=QtWidgets.QComboBox()
        self.formatCombox.setFixedWidth(180)
        self.formatCombox.addItems(['qt','avi','image'])

        self.button1=QtWidgets.QPushButton(u'��')
        self.button1.setFixedSize(100,20)
        self.button1.clicked.connect(self.openFile)
        self.button2=QtWidgets.QPushButton(u'���������')
        self.button2.setFixedSize(150,20)
        self.button2.clicked.connect(self.createCamera)
        self.button3=QtWidgets.QPushButton(u'K֡')
        self.button3.setFixedSize(100,20)
        self.button3.clicked.connect(self.K_Frame)
        self.button4=QtWidgets.QPushButton(u'ѡ��')
        self.button4.setFixedSize(100,20)
        self.button4.clicked.connect(self.ChoosePath)
        self.button5=QtWidgets.QPushButton(u'����')
        self.button5.setFixedSize(150,20)
        self.button5.clicked.connect(self.playBlase)
        self.button6=QtWidgets.QPushButton(u'�ر�')
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
        #K֡ǰ��ѡ�����
        cmds.select(CameraName,r=True)
        global i
        i=1
        #�ƶ�����ı任���ĵ���������
        cmds.move(0,0,0,CameraName+'.scalePivot',CameraName+'.rotatePivot',rpr=True)
        #�ƶ�ʱ�们��ͬʱ�任���λ��
        while i<=10:
            cmds.currentTime(5*i)
            i=i+1
            #ÿ�ƶ�һ��ʱ�们�飬�������Y��ת36�㣬��ת10��
            cmds.rotate(0,'36deg',0,r=True,os=True,fo=False,)
            #K֡
            cmds.setKeyframe()
    def ChoosePath(self):  #ȷ�����·��
        global nameAndPath
        nameAndPath=QtWidgets.QFileDialog.getSaveFileName(self,'Choose','C:\Users\Admin\Documents\maya','*.*;;*.avi;;*.mov;;*.image')
        self.saveFileLineEdit.setText(nameAndPath[0])
    def playBlase(self):
        #���� ���봴����������ӽ�
        cmds.lookThru(CameraName)
        #��������б�ǰ���ı�����(foramt)
        ComboxText=self.formatCombox.currentText()
        #�洢·�����ļ����� nameAndPath
        #����
        cmds.playblast(format=ComboxText,filename=nameAndPath[0])
    def Close(self):
        self.close()

ex = PB()
ex.show()
