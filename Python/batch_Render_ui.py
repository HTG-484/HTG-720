# -*- coding:utf-8 -*-
import sys
from PySide2 import QtWidgets
from PySide2 import QtCore,QtGui
import maya.cmds as cmds
class renderUI(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(renderUI,self).__init__(parent)
        self.resize(500,450)
        self.setWindowTitle('Render')
        self.mainLayout=QtWidgets.QGridLayout(self)
        self.createUI()
        self.arrangeLayout()
        self.Singal_Slot()
    def createUI(self):
        self.label_StartFrame=QtWidgets.QLabel('Start Frame')   #��ʼ֡
        self.label_EndFrame=QtWidgets.QLabel('End Frame')       #����֡
        self.label_ImageFormat=QtWidgets.QLabel('Image Format') #ͼƬ��ʽ
        self.label_RenderableCamera=QtWidgets.QLabel('Renderable Camere')  #ѡ�����
        self.label_Preset=QtWidgets.QLabel('Preset')            #Ԥ��(��С)
        self.label_Width=QtWidgets.QLabel('Width')              #���
        self.label_Height=QtWidgets.QLabel('Height')            #�߶�
        self.label_RenderingProgress=QtWidgets.QLabel('Rendering progress')  #��Ⱦ����
        self.label_OutputPath=QtWidgets.QLabel('Output Path')   #���·��
        
        self.line_StartFrame=QtWidgets.QLineEdit()              #��ʼ֡ �ı���
        self.line_EndFrame=QtWidgets.QLineEdit()                #����֡ �ı���
        self.line_Width=QtWidgets.QLineEdit()                   #����ı���
        self.line_Height=QtWidgets.QLineEdit()                  #�߶��ı���
        self.line_OutputPath=QtWidgets.QLineEdit()              #���·��
        
        self.progress_Rendering=QtWidgets.QProgressBar()         #��Ⱦ������
        self.button_OutputPath=QtWidgets.QPushButton('Choose')          #ѡ�����·��
        self.button_Render=QtWidgets.QPushButton('Render')      #��Ⱦ��ť
        self.button_Close=QtWidgets.QPushButton('Close')        #�رհ�ť
        #��Ⱦ�� ѡ�������б�
        self.combox_ImageFormat=QtWidgets.QComboBox()
        self.combox_ImageFormat.addItems(['JPEG','GIF','Maya iff'])
        #��Ⱦ��λ  ѡ�������б�
        self.combox_Rendercamera=QtWidgets.QComboBox()
                  #ѡ�񳡾�����������ı任�ڵ� 
        camera_list=cmds.listCameras()
        self.combox_Rendercamera.addItems(camera_list)
        #�����С  ѡ�������б�
        self.combox_Preset=QtWidgets.QComboBox()
        self.combox_Preset.addItems(['Custom',u'640��480','1k_Square','2k_Square','HD_540','HD_720','HD_1080'])    
    def arrangeLayout(self):
        self.mainLayout.addWidget(self.label_StartFrame,0,0)
        self.mainLayout.addWidget(self.line_StartFrame,0,1)
        self.mainLayout.addWidget(self.line_EndFrame,0,2)
        self.mainLayout.addWidget(self.label_EndFrame,0,3)
        self.mainLayout.addWidget(self.label_ImageFormat,1,0)
        self.mainLayout.addWidget(self.combox_ImageFormat,1,1)
        self.mainLayout.addWidget(self.label_RenderableCamera,2,0)
        self.mainLayout.addWidget(self.combox_Rendercamera,2,1)
        self.mainLayout.addWidget(self.label_Preset,3,0)
        self.mainLayout.addWidget(self.combox_Preset,3,1)
        self.mainLayout.addWidget(self.label_Width,4,0)
        self.mainLayout.addWidget(self.line_Width,4,1)
        self.mainLayout.addWidget(self.line_Height,4,2)
        self.mainLayout.addWidget(self.label_Height,4,3)
        self.mainLayout.addWidget(self.label_OutputPath,5,0)
        self.mainLayout.addWidget(self.line_OutputPath,5,1,1,2)
        self.mainLayout.addWidget(self.button_OutputPath,5,3)
        self.mainLayout.addWidget(self.label_RenderingProgress,6,0)
        self.mainLayout.addWidget(self.progress_Rendering,6,1,1,2)
        self.mainLayout.addWidget(self.button_Render,7,1)
        self.mainLayout.addWidget(self.button_Close,7,2)
    #�������֡��ͼƬ��ʽ���������Ϣ
    def get_Information(self):
        self.start_frame=int(self.line_StartFrame.text()) #�����ʼ֡��
        self.end_frame=int(self.line_EndFrame.text())     #��ý���֡��
        self.frames=(self.end_frame-self.start_frame)+1   #����֡��Ŀ
        self.render_using=self.combox_ImageFormat.currentText() #��ʽ�����б�  ��ǰ�ı�
        self.renderable_camera=self.combox_Rendercamera.currentText()#��������б�  ��ǰ�ı�
        self.image_Width=int(self.line_Width.text())
        self.image_Height=int(self.line_Height.text())
    #�ź����Ӳۺ���
    def Singal_Slot(self):
        #��Ⱦ��   �����б���ź���ۺ���������
        #self.combox_ImageFormat.currentIndex
        #��Ⱦ��λ �����б���ź���ۺ���������
        #�����С �����б���ź���ۺ���������
        self.combox_Preset.currentIndexChanged.connect(self.sizeChange)
        self.button_OutputPath.clicked.connect(self.choosePath)
        self.button_Render.clicked.connect(self.render)
        self.button_Close.clicked.connect(self.closeUI)
    #�ı������С
    def sizeChange(self):
        #��������б�ǰ����
        index=self.combox_Preset.currentIndex()
        if index!=0:
            if index==1:
                self.line_Width.setText('640')
                self.line_Height.setText('480')
            elif index==2:
                self.line_Width.setText('1024')
                self.line_Height.setText('1024')
            elif index==3:
                self.line_Width.setText('2048')
                self.line_Height.setText('2048')
            elif index==4:
                self.line_Width.setText('960')
                self.line_Height.setText('540')
            elif index==5:
                self.line_Width.setText('1280')
                self.line_Height.setText('720')
            elif index==6:
                self.line_Width.setText('1920')
                self.line_Height.setText('1080')
        else:
            self.line_Width.setText('')
            self.line_Height.setText('')
    def choosePath(self):
        choose_path=QtWidgets.QFileDialog.getSaveFileName(self,'Choose','C:\Users\Admin\Documents\maya','*.*;;*.JPEG;;*.GIF;;*.Maya iff')
        print choose_path
        self.line_OutputPath.setText(choose_path[0])
    def batch_Render(self):
        self.get_Information()
        cmds.render(self.renderable_camera,x=self.image_Width,y=self.image_Height)
    def closeUI(self):
        self.close()

render=renderUI()
render.show()