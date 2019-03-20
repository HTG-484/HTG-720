# -*- coding: utf-8 -*-

import sys
from PySide import QtWidgets
from PySide import QtCore,QtGui
import maya.cmds as cmds
import math

class Playblast(QDialog):
    def __init__(self, parent=None):

        super(Playblast, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.tr("360_Palyblast"))
        self.setGeometry(700, 400, 400, 350)

        select_file_button = QPushButton("SelectFilename")
        select_format_Label = QLabel("Outputformat")
        select_curren_Label = QLabel("Currenfram")
        select_over_Label = QLabel("Overfram")
        save_button = QPushButton("Save")
        close_button = QPushButton("Close")
        action_button = QPushButton("Actionplay")

        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QComboBox()
        self.lineEdit3 = QSpinBox()
        self.lineEdit4 = QSpinBox()
        self.lineEdit5 = QLineEdit()
        self.maxint = 2 ** 31
        self.lineEdit2.addItem(self.tr("movie"))
        self.lineEdit2.addItem(self.tr("avi"))
        self.lineEdit2.addItem(self.tr("qt"))
        self.lineEdit3.setRange(-self.maxint + 1, self.maxint - 1)
        self.lineEdit4.setRange(-self.maxint + 1, self.maxint - 1)
        global outfromat
        outfromat = self.lineEdit2.currentText()

        layout = QGridLayout()
        layout.addWidget(select_file_button, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(select_format_Label, 1, 0)
        layout.addWidget(self.lineEdit2, 1, 1)
        layout.addWidget(select_curren_Label, 2, 0)
        layout.addWidget(self.lineEdit3, 2, 1)
        layout.addWidget(select_over_Label, 3, 0)
        layout.addWidget(self.lineEdit4, 3, 1)
        layout.addWidget(save_button, 4, 0)
        layout.addWidget(self.lineEdit5, 4, 1)
        layout.addWidget(close_button,5,0)
        layout.addWidget(action_button, 5, 1)

        self.setLayout(layout)

        select_file_button.clicked.connect(self.slot_select_file_button)
        save_button.clicked.connect(self.slot_save_button)
        close_button.clicked.connect(self.slot_close_buton)
        action_button.clicked.connect(self.slot_action_button)

    def slot_select_file_button(self):
        global a
        a = QFileDialog.getOpenFileName(self, "Choose to shoot the screen FileName")
        openfile_tube = unicode(a)
        self.lineEdit1.setText(unicode(a[0]))
        cmds.file( query=True, lastTempFile=True)
        cmds.file(a[0], open=True)

    def slot_select_foramt_button(self):
        pass

    def slot_save_button(self):
        global save
        save = QFileDialog.getSaveFileName(self, "Save File", " ", "Video (*.qt *.mav *.avi)")
        savefile = unicode(save)
        self.lineEdit5.setText(unicode(save[0]))

    def slot_close_buton(self):
        self.close()

    def slot_action_button(self):
        cmds.select(ado=True)
        select_1 = cmds.ls(sl=True)

        x = 0
        y = 0
        z = 0
        for i in range(0, len(select_1), 1):
            cmds.select(select_1[i])
            b = cmds.xform(q=1, translation=1)
            x = b[0] + x
            y = b[1] + y
            z = b[2] + z
        p_x = x / len(select_1)
        p_y = y / len(select_1)
        p_z = z / len(select_1)

        f = 0
        for i in range(0, len(select_1), 1):
            cmds.select(select_1[i])
            b = cmds.xform(q=1, translation=1)
            x_1 = abs(b[0]) - p_x
            y_1 = abs(b[1]) - p_y
            z_1 = abs(b[2]) - p_z
            d = math.sqrt(x_1 ** 2 + y_1 ** 2 + z_1 ** 2)
            if d > f:
                f = d
        r = 5 * f
        c_x = p_x + r
        c_y = p_y
        c_z = p_z

        cmds.camera()
        cmds.move(c_x, c_y, c_z, "camera1")
        cmds.rotate(0, 90, 0, "camera1")
        cmds.move(p_x, p_y, p_z, "camera1.scalePivot", "camera1.rotatePivot")
        # 给摄像机Key关键帧
        cmds.currentTime(self.lineEdit3.value())
        cmds.rotate(-15, 0, 0, "camera1", r=1, os=1, fo=1)
        cmds.setKeyframe("camera1")
        cmds.currentTime(self.lineEdit4.value())
        cmds.rotate(-15, 360, 0, "camera1", r=1, os=1, fo=1)
        cmds.setKeyframe("camera1")
        # 进入摄像机视角
        cmds.lookThru("camera1")
        # palyblast存储位置
        local = save[0]
        print(local)
        cmds.playblast(format=outfromat, filename=local, sequenceTime=False, clearCache=True, viewer=True,
                       showOrnaments=True,
                       fp=4, percent=50, compression="H.264", quality=100)


if __name__ == "__main__":
    #app = QApplication(sys.argv)
    abc = Playblast()
    abc.show()
    #app.exec_()
