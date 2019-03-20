# -*- coding: utf-8 -*-

from PyQt5 import QtGui,QtCore

class widget():
    def __init__(self,parent = None):
        super(widget, self).__init__(parent)


    def initUI(self):
        a = [1,1,2,3,4]
        comboCheckBox = ComboCheckBox(a)




from PyQt5 import QComboBox,QLineEdit,QListWidget,QCheckBox,QListWidgetItem,QtWidgets
class ComboCheckBox(QComboBox):
    def __init__(self,items):#items==[str,str...]
        super(ComboCheckBox,self).__init__()
        self.items=items
        self.qCheckBox=[]
        self.qLineEdit=QLineEdit()
        self.qLineEdit.setReadOnly(True)
        qListWidget=QListWidget()
 
        self.row_num=len(self.items)
        for i in range(self.row_num):
            self.qCheckBox.append(QCheckBox())
            qItem=QListWidgetItem(qListWidget)
            self.qCheckBox[i].setText(self.items[i])
            qListWidget.setItemWidget(qItem,self.qCheckBox[i])
            self.qCheckBox[i].stateChanged.connect(self.show)
        
        self.setLineEdit(self.qLineEdit)         
        self.setModel(qListWidget.model())
        self.setView(qListWidget)
 
    def Selectlist(self):
        Outputlist=[]
        for i in range(self.row_num):
            if self.qCheckBox[i].isChecked()==True:
                Outputlist.append(self.qCheckBox[i].text())
        return Outputlist
 
    def show(self):
        show=''
        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clear()
        for i in self.Selectlist():
            show+=i+';'
        self.qLineEdit.setText(show)
        self.qLineEdit.setReadOnly(True)




# from PyQt5.QtWidgets import QComboBox,QLineEdit,QListWidget,QCheckBox,QListWidgetItem
 
# class ComboCheckBox(QComboBox):
#     def __init__(self,items):#items==[str,str...]
#         super(ComboCheckBox,self).__init__()
#         self.items=items
#         self.items.insert(0,'全部')
#         self.row_num=len(self.items)
#         self.Selectedrow_num=0
#         self.qCheckBox=[]
#         self.qLineEdit=QLineEdit()
#         self.qLineEdit.setReadOnly(True)
#         self.qListWidget=QListWidget()
#         self.addQCheckBox(0)
#         self.qCheckBox[0].stateChanged.connect(self.All)
#         for i in range(1,self.row_num):
#             self.addQCheckBox(i)
#             self.qCheckBox[i].stateChanged.connect(self.show)
#         self.setModel(self.qListWidget.model())
#         self.setView(self.qListWidget)
#         self.setLineEdit(self.qLineEdit)
#
#     def addQCheckBox(self,i):
#         self.qCheckBox.append(QCheckBox())
#         qItem=QListWidgetItem(self.qListWidget)
#         self.qCheckBox[i].setText(self.items[i])
#         self.qListWidget.setItemWidget(qItem,self.qCheckBox[i])
#
#     def Selectlist(self):
#         Outputlist=[]
#         for i in range(1,self.row_num):
#             if self.qCheckBox[i].isChecked()==True:
#                 Outputlist.append(self.qCheckBox[i].text())
#         self.Selectedrow_num=len(Outputlist)
#         return Outputlist
#
#     def show(self):
#         show=''
#         Outputlist=self.Selectlist()
#         self.qLineEdit.setReadOnly(False)
#         self.qLineEdit.clear()
#         for i in Outputlist:
#             show+=i+';'
#         if self.Selectedrow_num==0:
#             self.qCheckBox[0].setCheckState(0)
#         elif self.Selectedrow_num==self.row_num-1:
#             self.qCheckBox[0].setCheckState(2)
#         else:
#             self.qCheckBox[0].setCheckState(1)
#         self.qLineEdit.setText(show)
#         self.qLineEdit.setReadOnly(True)
#
#     def All(self,zhuangtai):
#         if zhuangtai==2:
#             for i in range(1,self.row_num):
#                 self.qCheckBox[i].setChecked(True)
#         elif zhuangtai==1:
#             if self.Selectedrow_num==0:
#                 self.qCheckBox[0].setCheckState(2)
#         elif zhuangtai==0:
#             self.clear()
#
#     def clear(self):
#         for i in range(self.row_num):
#             self.qCheckBox[i].setChecked(False)
