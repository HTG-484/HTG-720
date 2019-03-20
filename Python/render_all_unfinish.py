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
        self.commonSettings=Settings_common()  #实例化 三个类
        self.renderSetting=Settings_render()
        self.createUI()
    def createUI(self):
        #渲染层 标签
        label_Render_Layer=QtWidgets.QLabel('Render Layer')
        #渲染层 下拉列表
        combox_Render_Layer=QtWidgets.QComboBox()
        combox_Render_Layer.setFixedWidth(150)
        combox_Render_Layer.addItem('masterLayer')
        #渲染器 标签
        label_Render_Usinbg=QtWidgets.QLabel('Render Using')
        #渲染器 下拉列表
        combox_Render_Using=QtWidgets.QComboBox()
        combox_Render_Using.setFixedWidth(150)
        combox_Render_Using.addItems(['Maya Software','Maya Hardware 2.0','Maya Vector','Arnold Render'])
        #实例 一个很重要的布局
        layout_Mid=QtWidgets.QGridLayout()
        layout_Mid.addWidget(self.showPaging)
        #渲染按钮
        self.button_Render=QtWidgets.QPushButton('Render')
        self.button_Render.setFixedWidth(165)
        self.button_Render.clicked.connect(self.slot_render)
        #关闭按钮
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
#分页显示
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
        self.getCameras()    #在maya中调用，统计场景中可用相机
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
        #创建groupBox_File_Output里的控件
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
        self.slide_Quality=QtWidgets.QSlider(Qt.Horizontal) #Horizontal水平滑块控件,Vertical垂直滑块控件
        self.slide_Quality.setMaximum(100)
        self.slide_Quality.setMinimum(0)
        #创建groupBox_File_Output里的布局
        layout_File_Output=QtWidgets.QGridLayout(self.groupBox_File_Output)
        layout_File_Output.setContentsMargins(20,0,20,0)
        layout_File_Output.addWidget(label_File_Name,0,0)
        layout_File_Output.addWidget(line_File_Name,0,1,1,2)
        layout_File_Output.addWidget(label_Image_Format,1,0)
        layout_File_Output.addWidget(self.combox_Image_Format,1,1,1,2)
        layout_File_Output.addWidget(label_Quality,2,0)
        layout_File_Output.addWidget(self.line_Quality,2,1)
        layout_File_Output.addWidget(self.slide_Quality,2,2)

        #创建groupBox_Frame_Range里的控件
        label_Start_Frame=QtWidgets.QLabel('Start frame:')
        label_End_Frame=QtWidgets.QLabel('End frame:')
        label_By_Frame=QtWidgets.QLabel('By frame:')
        self.line_Start_Frame=QtWidgets.QLineEdit('1.000')
        self.line_End_Frame=QtWidgets.QLineEdit('10.000')
        self.line_By_Frame=QtWidgets.QLineEdit('10.000')
        self.line_By_Frame.setFocusPolicy(Qt.NoFocus)   #设置文本框不可获得焦点，即不可编辑 
        #创建groupBox_Frame_Range里的布局
        layout_Frame_Range=QtWidgets.QGridLayout(self.groupBox_Frame_Range)
        layout_Frame_Range.setContentsMargins(50,0,50,0)
        layout_Frame_Range.addWidget(label_Start_Frame,0,0)
        layout_Frame_Range.addWidget(self.line_Start_Frame,0,1)
        layout_Frame_Range.addWidget(label_End_Frame,1,0)
        layout_Frame_Range.addWidget(self.line_End_Frame,1,1)
        layout_Frame_Range.addWidget(label_By_Frame,2,0)
        layout_Frame_Range.addWidget(self.line_By_Frame,2,1)

        #创建groupBox_Renderable_Camera里的控件
        label_Renderable_Camera=QtWidgets.QLabel('Renderable Cameras')
        self.combox_Renderable_Camera=QtWidgets.QComboBox()
        #创建groupBox_Renderable_Camera里的布局
        layout_Renderable_Camera=QtWidgets.QGridLayout(self.groupBox_Renderable_Camera)
        layout_Renderable_Camera.setContentsMargins(50,0,50,0)
        layout_Renderable_Camera.addWidget(label_Renderable_Camera,0,0)
        layout_Renderable_Camera.addWidget(self.combox_Renderable_Camera,0,1)

        #创建groupBox_Image_Size里的控件
        label_Preset=QtWidgets.QLabel('Preset')            #预设(大小)
        label_Width=QtWidgets.QLabel('Width')              #宽度
        label_Height=QtWidgets.QLabel('Height')            #高度
        self.line_Width=QtWidgets.QLineEdit()                   #宽度文本框
        self.line_Width.setFixedWidth(80)
        self.line_Height=QtWidgets.QLineEdit()                  #高度文本框
        self.line_Height.setFixedWidth(80)
        self.combox_Preset=QtWidgets.QComboBox()                #输出大小  下拉列表
        self.combox_Preset.setFixedWidth(150)
        self.combox_Preset.addItems(['Custom',u'640×480','1k_Square','2k_Square','HD_540','HD_720','HD_1080'])
        #创建groupBox_Image_Size里的布局
        layout_Image_Size=QtWidgets.QGridLayout(self.groupBox_Image_Size)
        layout_Image_Size.setContentsMargins(50,0,50,0)
        layout_Image_Size.addWidget(label_Preset,0,0)
        layout_Image_Size.addWidget(self.combox_Preset,0,1)
        layout_Image_Size.addWidget(label_Width,1,0)
        layout_Image_Size.addWidget(self.line_Width,1,1)
        layout_Image_Size.addWidget(label_Height,2,0)
        layout_Image_Size.addWidget(self.line_Height,2,1)
    #更新Renderabel camera
    def getCameras(self):
        #listcamera 可选取场景中所有相机的变换节点名称
        camera_list=cmds.listCameras()
        #更新camera combox
        self.combox_Renderable_Camera.addItems(camera_list)
    #信号与槽函数的连接
    def singal_Slot(self):
        self.line_Start_Frame.editingFinished.connect(self.slot_frame)
        self.line_End_Frame.editingFinished.connect(self.slot_frame)
        #滑动slide时，更新文本框内的数值
        self.slide_Quality.valueChanged[int].connect(self.updateQuality)
        #改变image preset时，自动更新width、height
        self.combox_Preset.currentIndexChanged.connect(self.sizeChange)
    #获得图片格式、序列帧和相机的信息
    def get_Information(self):
        self.render_using=self.combox_Image_Format.currentText() #图片格式下拉列表  当前文本
        # self.quality_Value=int(self.line_Quality.text())   #获得渲染质量 数值
        # self.start_frame=float(self.line_Start_Frame.text()) #获得起始帧数   #finish
        # self.end_frame=float(self.line_End_Frame.text())     #获得结束帧数   #finish
        # self.renderable_camera=self.combox_Renderable_Camera.currentText()#相机下拉列表  当前文本
        # self.image_Width=int(self.line_Width.text())       #获得图片 宽
        # self.image_Height=int(self.line_Height.text())     #获得图片 高
    def slot_frame(self):
        self.start_frame=float(self.line_Start_Frame.text()) #获得起始帧数
        self.end_frame=float(self.line_End_Frame.text())     #获得结束帧数
        self.num=self.end_frame-self.start_frame+1
        self.line_By_Frame.setText(str(self.num))
        return self.num
    #更新quality滑块 数值
    def updateQuality(self,value):
        self.line_Quality.setText(str(value))
    #更新width、height
    def sizeChange(self):
        #相机下拉列表当前索引
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

        #实例化控件
        self.label_Output_Path=QtWidgets.QLabel('Path for Render Images')     #输出路径 label
        self.label_Output_Path.setFixedHeight(20)
        self.label_Output_Path.setAlignment(Qt.AlignCenter)
        self.label_Output_Path.setFont(QtGui.QFont("Roman times",10))
        self.label_Rendering_Progress=QtWidgets.QLabel('Rendering progress')  #渲染进度 label
        self.label_Rendering_Progress.setFixedHeight(20)
        self.label_Rendering_Progress.setAlignment(Qt.AlignCenter)
        self.label_Rendering_Progress.setFont(QtGui.QFont("Roman times",10))
        self.line_Output_Path=QtWidgets.QLineEdit()                          #输出路径 lineEdit
        self.line_Progress_Render=QtWidgets.QLineEdit()                       #进度 百分比
        self.line_Progress_Render.setFixedWidth(100)
        self.button_Output_Path=QtWidgets.QPushButton('Choose')             #选择路径按钮 button
        self.button_Output_Path.setFixedWidth(100)
        self.progress_Rendering=QtWidgets.QProgressBar(self)                    #渲染进度条 progress
        self.progress_Rendering.setFormat('%p')

        #布局
        self.mainLayout=QtWidgets.QVBoxLayout(self)
        self.mainLayout.addWidget(self.label_Output_Path)
        self.mainLayout.addWidget(self.line_Output_Path)
        self.mainLayout.addWidget(self.button_Output_Path)
        self.mainLayout.addWidget(self.label_Rendering_Progress)
        self.mainLayout.addWidget(self.progress_Rendering)
        self.mainLayout.addWidget(self.line_Progress_Render)

        #信号与槽
        self.button_Output_Path.clicked.connect(self.choosePath)
    def choosePath(self):
        choose_path=QtWidgets.QFileDialog.getSaveFileName(self,'Choose',r'C:\Users\Admin\Documents\maya','*.*;;*.JPEG;;*.GIF;;*.Maya iff')
        self.line_Output_Path.setText(choose_path[0])
render=RenderUI()
render.show()
