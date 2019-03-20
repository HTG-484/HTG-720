# -*- coding:utf-8 -*-
import sys
from PySide2 import QtWidgets
from PySide2 import QtCore,QtGui

#分页显示
class show_Paging(QtWidgets.QTabWidget):
    def __init__(self,parent=None):
        super(show_Paging, self).__init__(parent)
        commonSettings=Settings_common()
        renderSettings=Settings_render()
        self.addTab(commonSettings,'Common Settings')
        self.addTab(renderSettings,'Render Settings')
# common Settings
class Settings_common(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(Settings_common, self).__init__(parent)
        layout_common=QtWidgets.QVBoxLayout(self)

        tree_File_Output=QtWidgets.QTreeWidget() #根节点
        tree_File_Output.header().hide() #隐藏表头

        parent=QtWidgets.QTreeWidgetItem(tree_File_Output) #指出父节点
        parent.setText(0,'File Output')

        parent_child1_1=QtWidgets.QTreeWidgetItem(parent)

        parent_child1_1.setText(0,'File name prefix:')

        parent_child2=QtWidgets.QTreeWidgetItem(parent)
        parent_child2.setText(0,'Image format:')

        layout_common.addWidget(tree_File_Output)
        # self.setLayout(layout_common)


# render Settings
class Settings_render(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(Settings_render, self).__init__(parent)

class renderUI(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(renderUI, self).__init__(parent)
        self.setWindowTitle(u'Batch_Render')
        self.resize(400,450)
        self.mainLayout=QtWidgets.QGridLayout(self)
        self.showPaging=show_Paging()
        self.createUI()
    def createUI(self):
        #渲染层 标签
        label_Render_Layer=QtWidgets.QLabel('Render Layer')
        #渲染层 下拉列表
        combox_Render_Layer=QtWidgets.QComboBox()
        #渲染器 标签
        label_Render_Usinbg=QtWidgets.QLabel('Render Using')
        #渲染器 下拉列表
        combox_Render_Using=QtWidgets.QComboBox()
        #实例 一个很重要的布局
        layout_Mid=QtWidgets.QGridLayout()
        layout_Mid.addWidget(self.showPaging)
        #渲染按钮
        button_Render=QtWidgets.QPushButton('Render')
        #关闭按钮
        button_Close=QtWidgets.QPushButton('close')

        self.mainLayout.addWidget(label_Render_Layer,0,0)
        self.mainLayout.addWidget(combox_Render_Layer,0,1)
        self.mainLayout.addWidget(label_Render_Usinbg,1,0)
        self.mainLayout.addWidget(combox_Render_Using,1,1)
        self.mainLayout.addLayout(layout_Mid,2,0,4,4)
        self.mainLayout.addWidget(button_Render,7,0,1,2)
        self.mainLayout.addWidget(button_Close,7,2,1,2)



        self.setLayout(self.mainLayout)




app = QtWidgets.QApplication(sys.argv)
render=renderUI()
render.show()
app.exec_()
