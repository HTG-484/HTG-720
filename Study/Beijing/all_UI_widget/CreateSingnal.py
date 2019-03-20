# # -*- coding:utf-8 -*-
# import sys
# from PyQt5.QtCore import pyqtSignal, QObject
# from PyQt5.QtWidgets import *
# import sys
# import os
#
#
# class Communicate(QObject):  # 信号使用了pyqtSignal()方法创建，
#     # 并且成为外部类Communicate类的属性。
#
#     closeApp = pyqtSignal()  # 创建一个新的信号叫做closeApp
#
#
# class Button(QPushButton):
#     def __init__(self,text,parent = None):
#         super(Button, self).__init__(parent)
#
#         self.setText(text)
#         self.signal = pyqtSignal()
#
#
# class Example(QMainWindow):
#     def __init__(self,parent = None):
#         QMainWindow.__init__(self,parent)
#
#         self.my_UI()
#
#     def my_UI(self):
#         self.button = Button('nihao',self)
#         self.button.move(100,100)
#         self.c = Communicate()
#         self.c.closeApp.connect(self.close)  # 把自定义的closeApp信号连接到QMainWindow的close()槽上。
#         self.button.signal.connect(self.aaa)
#         self.setGeometry(300, 300, 290, 150)
#         self.setWindowTitle('发出信号')
#         self.show()
#
#     def mousePressEvent(self, event):
#         self.c.closeApp.emit()  # 在窗口上点击一下鼠标，closeApp信号会被发射
#
#     def aaa(self):
#         #self.button.signal.emit()
#         print('aaa')
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())
# coding: utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys


class StringListDlg(QDialog):
    """
    主对话框
    """

    def __init__(self, fruit, parent=None):
        super(StringListDlg, self).__init__(parent)
        self.fruit = fruit
        # 字符串列表
        self.fruits = QListWidget()
        # for f in self.fruit:
        #    self.fruits.addItem(QListWidgetItem(f))
        self.fruits.addItems(fruit)
        # 按钮
        self.btn_add = QPushButton('&Add...')
        self.btn_add.setEnabled(False)
        btn_edit = QPushButton('&Edit...')
        #btn_edit.setEnabled(False)
        btn_remove = QPushButton('&Remove...')
        btn_up = QPushButton('&Up')
        btn_down = QPushButton('&Down')
        btn_sort = QPushButton('&Sort')
        btn_close = QPushButton('&Close')
        # 垂直布局
        v_box = QVBoxLayout()
        v_box.addWidget(self.btn_add)
        v_box.addWidget(btn_edit)
        v_box.addWidget(btn_remove)
        v_box.addWidget(btn_up)
        v_box.addWidget(btn_down)
        v_box.addWidget(btn_sort)
        v_box.addStretch(1)
        v_box.addWidget(btn_close)
        # 水平布局
        h_box = QHBoxLayout()
        h_box.addWidget(self.fruits)
        h_box.addLayout(v_box)
        # 设置布局
        self.setLayout(h_box)
        self.resize(QSize(400, 300))
        self.setWindowTitle(u'水果')
        # 连接信号和槽
        self.btn_add.clicked.connect(self.add)
        btn_edit.clicked.connect(self.edit)
        btn_remove.clicked.connect(self.remove)
        btn_up.clicked.connect(self.up)
        btn_down.clicked.connect(self.down)
        btn_sort.clicked.connect(self.sort)
        btn_close.clicked.connect(self.close)
        self.fruits.itemClicked.connect((self.BtnState))

    def BtnState(self):
        self.btn_add.setEnabled(True)

    # 定义槽
    def add(self):
        # 添加
        add = FruitDlg('Add fruit', self)
        self.fruits.addItem('333')
        self.fruits.insertItem(10,'30')
        if add.exec_():
            fruit_added = add.fruit
            self.fruits.addItem(fruit_added)
            print(fruit_added)

    def edit(self):
        # 编辑
        row = self.fruits.currentRow()
        fruit = self.fruits.takeItem(row)
        edit = FruitDlg('Edit fruit', fruit.text(), self)
        if edit.exec_():
            print(edit.fruit)
            self.fruits.addItem(edit.fruit)

    def remove(self):
        # 移除
        if QMessageBox.warning(self, u'确认', u'确定要删除?', QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
            item_deleted = self.fruits.takeItem(self.fruits.currentRow())
            # 将读取的值设置为None
            item_deleted = None

    def up(self):
        # 上移
        # 当前元素索引
        index = self.fruits.currentRow()
        if index > 0:
            # 索引号减1
            index_new = index - 1
            # 取元素值，并在新索引位置插入
            self.fruits.insertItem(index_new, self.fruits.takeItem(self.fruits.currentRow()))
            # 设置当前元素索引为新插入位置，可以使得元素连续上移
            self.fruits.setCurrentRow(index_new)

    def down(self):
        # 下移
        index = self.fruits.currentRow()
        if index < self.fruits.count():
            index_new = index + 1
            self.fruits.insertItem(index_new, self.fruits.takeItem(self.fruits.currentRow()))
            self.fruits.setCurrentRow(index_new)

    def sort(self):
        # 排序
        self.fruits.sortItems(Qt.AscendingOrder)

    def close(self):
        # 退出
        self.done(0)


# 弹出对话框
# add
class FruitDlg(QDialog):
    def __init__(self, title, fruit=None, parent=None):
        super(FruitDlg, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # label_0 = QLabel(u'Add fruit： 譬如苹果，香蕉，橘子，西瓜，火龙果，枣，梨子，榴莲')
        label_0 = QLabel(title)
        # 让标签字换行
        label_0.setWordWrap(True)
        self.fruit_edit = QLineEdit(fruit)
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        validator = QRegExp(r'[^\s][\w\s]+')
        self.fruit_edit.setValidator(QRegExpValidator(validator, self))

        v_box = QVBoxLayout()
        v_box.addWidget(label_0)
        v_box.addWidget(self.fruit_edit)
        v_box.addWidget(btns)
        self.setLayout(v_box)

        self.fruit = None

    def accept(self):
        # OK按钮
        self.fruit = unicode(self.fruit_edit.text())
        # self.done(0)
        QDialog.accept(self)

    def reject(self):
        # self.done(1)
        QDialog.reject(self)


# edit
# remove confirm

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fruit = ["Banana", " a ", " a ", "Clementine", "Fig", "Guava", "Mango", "Honeydew Melon",
             "Date", "Watermelon", "Tangerine", "Ugli Fruit", "Juniperberry", "Kiwi",
             "Lemon", "Nectarine", "Plum", "Raspberry", "Strawberry", "Orange"]
    s = StringListDlg(fruit)
    s.show()
    app.exec_()
