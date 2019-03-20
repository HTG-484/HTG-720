# -*- coding:utf-8 -*-
import sys
import maya.cmds as cmds
from PySide2 import QtWidgets
from PySide2 import QtGui,QtCore
from PySide2.QtCore import Qt
class RenderUI(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(RenderUI, self).__init__(parent)
        self.setWindowTitle(u'Batch_Render')
        self.setFixedSize(350,420)
        self.mainLayout=QtWidgets.QGridLayout(self)
        self.showPaging=show_Paging()
        self.commonSettings=Settings_common()  #ʵ���� ������
        self.renderSetting=Settings_render()
        self.createUI()
    def createUI(self):
        #��Ⱦ�� ��ǩ
        label_Render_Layer=QtWidgets.QLabel('Render Layer')
        #��Ⱦ�� �����б�
        combox_Render_Layer=QtWidgets.QComboBox()
        combox_Render_Layer.setFixedWidth(150)
        combox_Render_Layer.addItem('masterLayer')
        #��Ⱦ�� ��ǩ
        label_Render_Usinbg=QtWidgets.QLabel('Render Using')
        #��Ⱦ�� �����б�
        combox_Render_Using=QtWidgets.QComboBox()
        combox_Render_Using.setFixedWidth(150)
        combox_Render_Using.addItems(['Maya Software','Maya Hardware 2.0','Maya Vector','Arnold Render'])
        #ʵ�� һ������Ҫ�Ĳ���
        layout_Mid=QtWidgets.QGridLayout()
        layout_Mid.addWidget(self.showPaging)
        #��Ⱦ��ť
        self.button_Render=QtWidgets.QPushButton('Render')
        self.button_Render.setFixedWidth(165)
        self.button_Render.clicked.connect(self.slot_render)
        #�رհ�ť
        self.button_Close=QtWidgets.QPushButton('close')
        self.button_Close.setFixedWidth(165)
        self.button_Close.clicked.connect(self.slot_close)
        
        self.mainLayout.addWidget(label_Render_Layer,0,0)
        self.mainLayout.addWidget(combox_Render_Layer,0,1)
        self.mainLayout.addWidget(label_Render_Usinbg,1,0)
        self.mainLayout.addWidget(combox_Render_Using,1,1)
        self.mainLayout.addLayout(layout_Mid,2,0,4,4)
        self.mainLayout.addWidget(self.button_Render,7,0,1,2)
        self.mainLayout.addWidget(self.button_Close,7,2,1,2)
    def slot_render(self):
        num=int(self.commonSettings.slot_frame())
        self.renderSetting.progress_Rendering.setMinimum(0)
        self.renderSetting.progress_Rendering.setMaximum(num)
        for i in range(num):
            self.renderSetting.progress_Rendering.setValue(i)
    def slot_close(self):
        self.close()
#��ҳ��ʾ
class show_Paging(QtWidgets.QTabWidget):
    def __init__(self,parent=None):
        super(show_Paging, self).__init__(parent)
        commonSettings=Settings_common()
        renderSettings=Settings_render()
        self.addTab(commonSettings,'Common Settings')
        self.addTab(renderSettings,'Render Settings')
# common Settings
class Settings_common(QtWidgets.QToolBox):
    def __init__(self,parent=None):
        super(Settings_common, self).__init__(parent)
        self.createGroupBox()
        self.createWidgets()
        self.getCameras()    #��maya�е��ã�ͳ�Ƴ����п������
        self.singal_Slot()
        self.get_Information()
    def createGroupBox(self):
        self.groupBox_File_Output=QtWidgets.QGroupBox()
        self.groupBox_Frame_Range=QtWidgets.QGroupBox()
        self.groupBox_Renderable_Camera=QtWidgets.QGroupBox()
        self.groupBox_Image_Size=QtWidgets.QGroupBox()
        self.addItem(self.groupBox_File_Output,'File Output')
        self.addItem(self.groupBox_Frame_Range,'Frame Range')
        self.addItem(self.groupBox_Renderable_Camera,'Renderable Cameras')
        self.addItem(self.groupBox_Image_Size,'Image Size')
    def createWidgets(self):
        #����groupBox_File_Output��Ŀؼ�
        label_File_Name=QtWidgets.QLabel('File name prefix:')
        line_File_Name=QtWidgets.QLineEdit('(not set;using scence name)')
        line_File_Name.setFixedWidth(170)
        label_Image_Format=QtWidgets.QLabel('image format:')
        self.combox_Image_Format=QtWidgets.QComboBox()
        self.combox_Image_Format.setFixedWidth(100)
        self.combox_Image_Format.addItems(['JPEG','GIF','Maya iff'])
        label_Quality=QtWidgets.QLabel('Quality')
        self.line_Quality=QtWidgets.QLineEdit('0')
        self.line_Quality.setFixedWidth(50)
        self.slide_Quality=QtWidgets.QSlider(Qt.Horizontal) #Horizontalˮƽ����ؼ�,Vertical��ֱ����ؼ�
        self.slide_Quality.setMaximum(100)
        self.slide_Quality.setMinimum(0)
        #����groupBox_File_Output��Ĳ���
        layout_File_Output=QtWidgets.QGridLayout(self.groupBox_File_Output)
        layout_File_Output.setContentsMargins(20,0,20,0)
        layout_File_Output.addWidget(label_File_Name,0,0)
        layout_File_Output.addWidget(line_File_Name,0,1,1,2)
        layout_File_Output.addWidget(label_Image_Format,1,0)
        layout_File_Output.addWidget(self.combox_Image_Format,1,1,1,2)
        layout_File_Output.addWidget(label_Quality,2,0)
        layout_File_Output.addWidget(self.line_Quality,2,1)
        layout_File_Output.addWidget(self.slide_Quality,2,2)

        #����groupBox_Frame_Range��Ŀؼ�
        label_Start_Frame=QtWidgets.QLabel('Start frame:')
        label_End_Frame=QtWidgets.QLabel('End frame:')
        label_By_Frame=QtWidgets.QLabel('By frame:')
        self.line_Start_Frame=QtWidgets.QLineEdit('1.000')
        self.line_End_Frame=QtWidgets.QLineEdit('10.000')
        self.line_By_Frame=QtWidgets.QLineEdit('10.000')
        self.line_By_Frame.setFocusPolicy(Qt.NoFocus)   #�����ı��򲻿ɻ�ý��㣬�����ɱ༭ 
        #����groupBox_Frame_Range��Ĳ���
        layout_Frame_Range=QtWidgets.QGridLayout(self.groupBox_Frame_Range)
        layout_Frame_Range.setContentsMargins(50,0,50,0)
        layout_Frame_Range.addWidget(label_Start_Frame,0,0)
        layout_Frame_Range.addWidget(self.line_Start_Frame,0,1)
        layout_Frame_Range.addWidget(label_End_Frame,1,0)
        layout_Frame_Range.addWidget(self.line_End_Frame,1,1)
        layout_Frame_Range.addWidget(label_By_Frame,2,0)
        layout_Frame_Range.addWidget(self.line_By_Frame,2,1)

        #����groupBox_Renderable_Camera��Ŀؼ�
        label_Renderable_Camera=QtWidgets.QLabel('Renderable Cameras')
        self.combox_Renderable_Camera=QtWidgets.QComboBox()
        #����groupBox_Renderable_Camera��Ĳ���
        layout_Renderable_Camera=QtWidgets.QGridLayout(self.groupBox_Renderable_Camera)
        layout_Renderable_Camera.setContentsMargins(50,0,50,0)
        layout_Renderable_Camera.addWidget(label_Renderable_Camera,0,0)
        layout_Renderable_Camera.addWidget(self.combox_Renderable_Camera,0,1)

        #����groupBox_Image_Size��Ŀؼ�
        label_Preset=QtWidgets.QLabel('Preset')            #Ԥ��(��С)
        label_Width=QtWidgets.QLabel('Width')              #���
        label_Height=QtWidgets.QLabel('Height')            #�߶�
        self.line_Width=QtWidgets.QLineEdit()                   #����ı���
        self.line_Width.setFixedWidth(80)
        self.line_Height=QtWidgets.QLineEdit()                  #�߶��ı���
        self.line_Height.setFixedWidth(80)
        self.combox_Preset=QtWidgets.QComboBox()                #�����С  �����б�
        self.combox_Preset.setFixedWidth(150)
        self.combox_Preset.addItems(['Custom',u'640��480','1k_Square','2k_Square','HD_540','HD_720','HD_1080'])
        #����groupBox_Image_Size��Ĳ���
        layout_Image_Size=QtWidgets.QGridLayout(self.groupBox_Image_Size)
        layout_Image_Size.setContentsMargins(50,0,50,0)
        layout_Image_Size.addWidget(label_Preset,0,0)
        layout_Image_Size.addWidget(self.combox_Preset,0,1)
        layout_Image_Size.addWidget(label_Width,1,0)
        layout_Image_Size.addWidget(self.line_Width,1,1)
        layout_Image_Size.addWidget(label_Height,2,0)
        layout_Image_Size.addWidget(self.line_Height,2,1)
    #����Renderabel camera
    def getCameras(self):
        #listcamera ��ѡȡ��������������ı任�ڵ�����
        camera_list=cmds.listCameras()
        #����camera combox
        self.combox_Renderable_Camera.addItems(camera_list)
    #�ź���ۺ���������
    def singal_Slot(self):
        self.line_Start_Frame.editingFinished.connect(self.slot_frame)
        self.line_End_Frame.editingFinished.connect(self.slot_frame)
        #����slideʱ�������ı����ڵ���ֵ
        self.slide_Quality.valueChanged[int].connect(self.updateQuality)
        #�ı�image presetʱ���Զ�����width��height
        self.combox_Preset.currentIndexChanged.connect(self.sizeChange)
    #���ͼƬ��ʽ������֡���������Ϣ
    def get_Information(self):
        self.render_using=self.combox_Image_Format.currentText() #ͼƬ��ʽ�����б�  ��ǰ�ı�
        # self.quality_Value=int(self.line_Quality.text())   #�����Ⱦ���� ��ֵ
        # self.start_frame=float(self.line_Start_Frame.text()) #�����ʼ֡��   #finish
        # self.end_frame=float(self.line_End_Frame.text())     #��ý���֡��   #finish
        # self.renderable_camera=self.combox_Renderable_Camera.currentText()#��������б�  ��ǰ�ı�
        # self.image_Width=int(self.line_Width.text())       #���ͼƬ ��
        # self.image_Height=int(self.line_Height.text())     #���ͼƬ ��
    def slot_frame(self):
        self.start_frame=float(self.line_Start_Frame.text()) #�����ʼ֡��
        self.end_frame=float(self.line_End_Frame.text())     #��ý���֡��
        self.num=self.end_frame-self.start_frame+1
        self.line_By_Frame.setText(str(self.num))
        return self.num
    #����quality���� ��ֵ
    def updateQuality(self,value):
        self.line_Quality.setText(str(value))
    #����width��height
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
# render Settings
class Settings_render(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(Settings_render, self).__init__(parent)

        #ʵ�����ؼ�
        self.label_Output_Path=QtWidgets.QLabel('Path for Render Images')     #���·�� label
        self.label_Output_Path.setFixedHeight(20)
        self.label_Output_Path.setAlignment(Qt.AlignCenter)
        self.label_Output_Path.setFont(QtGui.QFont("Roman times",10))
        self.label_Rendering_Progress=QtWidgets.QLabel('Rendering progress')  #��Ⱦ���� label
        self.label_Rendering_Progress.setFixedHeight(20)
        self.label_Rendering_Progress.setAlignment(Qt.AlignCenter)
        self.label_Rendering_Progress.setFont(QtGui.QFont("Roman times",10))
        self.line_Output_Path=QtWidgets.QLineEdit()                          #���·�� lineEdit
        self.line_Progress_Render=QtWidgets.QLineEdit()                       #���� �ٷֱ�
        self.line_Progress_Render.setFixedWidth(100)
        self.button_Output_Path=QtWidgets.QPushButton('Choose')             #ѡ��·����ť button
        self.button_Output_Path.setFixedWidth(100)
        self.progress_Rendering=QtWidgets.QProgressBar(self)                    #��Ⱦ������ progress
        self.progress_Rendering.setFormat('%p')

        #����
        self.mainLayout=QtWidgets.QVBoxLayout(self)
        self.mainLayout.addWidget(self.label_Output_Path)
        self.mainLayout.addWidget(self.line_Output_Path)
        self.mainLayout.addWidget(self.button_Output_Path)
        self.mainLayout.addWidget(self.label_Rendering_Progress)
        self.mainLayout.addWidget(self.progress_Rendering)
        self.mainLayout.addWidget(self.line_Progress_Render)

        #�ź����
        self.button_Output_Path.clicked.connect(self.choosePath)
    def choosePath(self):
        choose_path=QtWidgets.QFileDialog.getSaveFileName(self,'Choose',r'C:\Users\Admin\Documents\maya','*.*;;*.JPEG;;*.GIF;;*.Maya iff')
        self.line_Output_Path.setText(choose_path[0])
render=RenderUI()
render.show()
