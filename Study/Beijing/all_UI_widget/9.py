# coding: utf-8 
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class mat(QDialog):
    def __init__(self):
        super(mat, self).__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle(u"用户信息")
        self.setWindowFlags(Qt.Window)
        
        label1=QLabel(u"用户名：")
        label2=QLabel(u"姓名：")
        label3=QLabel(u"性别：")
        label4=QLabel(u"部门：")
        label5=QLabel(u"年龄：")
        otherLabel=QLabel(u"备注")
        otherLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        useedit=QLineEdit()
        nameedit=QLineEdit()
        sexcom=QComboBox()
        sexcom.insertItem(0,u"男")
        sexcom.insertItem(1,u"女")
        depart=QTextEdit()
        ageedit=QLineEdit()
        labelCol=0
        contentCol=1
        leftLayout=QGridLayout()
        leftLayout.addWidget(label1,0,labelCol)
        leftLayout.addWidget(useedit,0,contentCol)
        leftLayout.addWidget(label2,1,labelCol)
        leftLayout.addWidget(nameedit,1,contentCol)
        leftLayout.addWidget(label3,2,labelCol)
        leftLayout.addWidget(sexcom,2,contentCol)
        leftLayout.addWidget(label4,3,labelCol)
        leftLayout.addWidget(depart,3,contentCol)
        leftLayout.addWidget(label5,4,labelCol)
        leftLayout.addWidget(ageedit,4,contentCol)
        leftLayout.addWidget(otherLabel,5,labelCol,1,2)
        leftLayout.setColumnStretch(0,1)
        leftLayout.setColumnStretch(1,3)

        
        label6=QLabel(u"头像")
        iconLabel=QLabel()
        icon=QPixmap("Nuke\Library\2.jpg")
        pixmap = icon.scaledToWidth(150)
        print pixmap
        
        iconLabel.setPixmap(pixmap)
        
        iconPushButton=QPushButton(u"改变")
        hlay=QHBoxLayout()
        hlay.setSpacing(20)
        hlay.addWidget(label6)
        hlay.addWidget(iconLabel)
        hlay.addWidget(iconPushButton)

        
        label7=QLabel(u"个人说明:")
        descTextEdit=QTextEdit()
        rightLayout=QVBoxLayout()
        rightLayout.setMargin(10)
        rightLayout.addLayout(hlay)
        rightLayout.addWidget(label7)
        rightLayout.addWidget(descTextEdit)
        
        

        OKPushButton=QPushButton(u"确定")
        cancelPushButton=QPushButton(u"取消")
        bottomLayout=QHBoxLayout()
        bottomLayout.addStretch()
        bottomLayout.addWidget(OKPushButton)
        bottomLayout.addWidget(cancelPushButton)

        mainLayout=QGridLayout(self)
        mainLayout.setMargin(15)
        mainLayout.setSpacing(10)
        mainLayout.addLayout(leftLayout,0,0)
        mainLayout.addLayout(rightLayout,0,1)
        mainLayout.addLayout(bottomLayout,1,0,1,2)
        #mainLayout.setSizeConstraint(QLayout.SetFixedSize)       


        self.setLayout(leftLayout)
        

def main():

    app = QApplication(sys.argv)
    ex = mat()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()
