# -*- coding:utf-8 -*-
from PySide2 import QtWidgets
import sys

class RenderUI(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(RenderUI, self).__init__(parent)
        self.setWindowTitle(u'Batch_Render')
        self.resize(400,450)
        self.mainLayout=QtWidgets.QVBoxLayout()
        # self.showPaging=show_Paging()
        self.createUI()
        # self.tree = Settings_common()
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
        # layout_Mid.addWidget(self.showPaging)
        #渲染按钮
        button_Render=QtWidgets.QPushButton('Render')
        #关闭按钮
        button_Close=QtWidgets.QPushButton('close')


        layout_common=QtWidgets.QVBoxLayout()
        tree_File_Output=QtWidgets.QTreeWidget() #根节点
        tree_File_Output.header().hide() #隐藏表头

        parent=QtWidgets.QTreeWidgetItem(tree_File_Output) #指出父节点
        parent.setText(0,'File Output')

        parent_child1_1=QtWidgets.QTreeWidgetItem(parent)
        # print("111111")
        parent_child1_1.setText(0,'File name prefix:')

        parent_child2=QtWidgets.QTreeWidgetItem(parent)
        parent_child2.setText(0,'Image format:')
        layout_common.addWidget(tree_File_Output)



        # self.mainLayout.addWidget(label_Render_Layer,0,0)
        # self.mainLayout.addWidget(combox_Render_Layer,0,1)
        # self.mainLayout.addWidget(label_Render_Usinbg,1,0)
        # self.mainLayout.addWidget(combox_Render_Using,1,1)
        # self.mainLayout.addLayout(layout_Mid,2,0,4,4)
        # self.mainLayout.addWidget(button_Render,7,0,1,2)
        # self.mainLayout.addWidget(button_Close,7,2,1,2)
        self.mainLayout.addWidget(label_Render_Layer)
        self.mainLayout.addWidget(combox_Render_Layer)
        self.mainLayout.addWidget(label_Render_Usinbg)
        self.mainLayout.addWidget(combox_Render_Using)
        self.mainLayout.addLayout(layout_common)
        self.mainLayout.addWidget(label_Render_Usinbg)






        self.setLayout(self.mainLayout)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = RenderUI()
    window.show()
    app.exec_()