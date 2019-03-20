# coding=utf-8
import sys
from functools import partial
from PySide.QtCore import *
from PySide.QtGui import *
# from PySide.QtCore import Signal


class popup_win(QWidget):
    def __init__(self, parent=None):
        super(popup_win, self).__init__(parent)
        self.setWindowFlags(Qt.Popup)  # 抛出一个弹窗


class Communicate(QObject):
    my_signal = Signal(list)


class main_view(QDialog):
    def __init__(self, parent=None):
        super(main_view, self).__init__(parent)
        self.frame = QFrame(self)
        self.frame.setWindowTitle(u"设置类型权限")
        self.frame.setGeometry(QRect(20, 0, 461, 140))  # 设置QFrame的位置，以及长宽

        self.setFocusPolicy(Qt.ClickFocus)
         # 实例化弹窗

        # 创建一个QListWidget，QToolButton 把他们放到QFrame里
        self.textEdit = QListWidget(self.frame)
        self.textEdit.setViewMode(QListView.IconMode)
        self.textEdit.setGeometry(QRect(0, 10, 425, 120))  # 设置QListWidget的位置，以及长宽

        self.toolButton = QToolButton(self.frame)
        self.toolButton.setIcon(QIcon("D:/text/images.jpg"))  # 给QToolButton添加图片
        self.toolButton.setIconSize(QSize(100, 300))  # 设置图片的大小
        list_name = []
        self.toolButton.clicked.connect(partial(self.cast_window, list_name))   # 点击self.toolButton调用槽函数self.cast_window，弹出一个弹窗



        self.toolButton.setGeometry(QRect(425, 10, 37, 121))  # 设置self.toolButton的位置，以及长宽

    def cast_window(self, list_name):
        self.list_name = list_name
        self.popup_window = QDialog()
        self.popup_layout = QVBoxLayout(self.popup_window)  # 设置布局为V布局
        self.list_widget = QListWidget()
        # self.list_widget.setViewMode(QListView.IconMode)
        self.popup_layout.addWidget(self.list_widget)


        # 创建布局里的控件QCheckBox
        list = [u"导演", u"管理员", u"组长"]
        if len(self.list_name) > 0:

            for name in self.list_name:
                new_item = QListWidgetItem()
                new_item.setText(name)
                new_item.setCheckState(Qt.Unchecked)
                self.list_widget.addItem(new_item)

        for name in list:
            new_item = QListWidgetItem()
            new_item.setText(name)
            new_item.setCheckState(Qt.Unchecked)
            self.list_widget.addItem(new_item)

        self.list_widget.itemClicked.connect(self.add_item_there)
        # self.connect(self.list_widget, SIGNAL("itemClicked(QListWidgetItem*)"), self.delete_item)

        new_item_three = QListWidgetItem()
        self.list_widget.addItem(new_item_three)
        widget = QWidget()
        widget_Text = QLabel(u"添加更多选项")
        widget_Button_tow = QPushButton("+")
        widget_Button_tow.clicked.connect(self.add)
        widget_Layout = QHBoxLayout()
        # widget_Layout.setMargin(0)
        widget_Layout.addWidget(widget_Text)
        widget_Layout.addWidget(widget_Button_tow)
        widget_Layout.addStretch()
        widget_Layout.setSizeConstraint(QLayout.SetFixedSize)
        widget.setLayout(widget_Layout)
        new_item_three.setSizeHint(widget.sizeHint())
        self.list_widget.setItemWidget(new_item_three, widget)

        mouse_xy = self.toolButton.mapToGlobal(self.toolButton.pos())  # 获取self.toolButton的相对位置
        x = mouse_xy.x()-400
        y = mouse_xy.y()+110
        self.popup_window.move(x, y)  # 移动self.popup_window的位置，通过改x，y的值
        self.popup_window.show()  # 显示抛出的窗口

    def add_item_there(self, event):
        name = event.text()
        new_item_three = QListWidgetItem()
        num_tow = self.textEdit.count()
        if event.checkState():

            self.textEdit.addItem(new_item_three)
            widget = QWidget()
            widget_Text = QLabel(name)
            widget_Button_tow = QPushButton("X")
            widget_Button_tow.clicked.connect(partial(self.delete_item, new_item_three))
            widget_Layout = QHBoxLayout()
            # widget_Layout.setMargin(0)
            widget_Layout.addWidget(widget_Text)
            widget_Layout.addWidget(widget_Button_tow)
            widget_Layout.addStretch()
            widget_Layout.setSizeConstraint(QLayout.SetFixedSize)
            widget.setLayout(widget_Layout)
            new_item_three.setSizeHint(widget.sizeHint())
            self.textEdit.setItemWidget(new_item_three, widget)
        else:

            self.textEdit.takeItem(num_tow-1)

    def delete_item(self, item):
        num = self.textEdit.row(item)  # 获取当前项目的索引
        self.textEdit.takeItem(num)

    def add(self):
        print "add"
        self.bb = main_view1()
        self.bb.show()
        self.bb.world.my_signal.connect(self.cast_window)

class main_view1(QListWidget):
    def __init__(self, parent=None):
        super(main_view1, self).__init__(parent)
        self.world = Communicate()
        self.setFocusPolicy(Qt.StrongFocus)
        # 创建布局里的控件QCheckBox
        list = [u"法哥", u"金哥", u"世明哥", u"德明哥", u"灿哥", u"瑞恳", u"飞哥"]

        for name in list:
            new_item = QListWidgetItem()
            new_item.setText(name)
            new_item.setCheckState(Qt.Unchecked)
            self.addItem(new_item)

        new_item_three = QListWidgetItem()
        self.addItem(new_item_three)
        widget_Button_tow = QPushButton(u"选中添加并关闭此窗口")
        widget_Button_tow.clicked.connect(self.send)
        widget_Button_tow.clicked.connect(self.close1)
        new_item_three.setSizeHint(widget_Button_tow.sizeHint())
        self.setItemWidget(new_item_three, widget_Button_tow)

        self.itemClicked.connect(self.list_item)
        x = 600
        y = 450
        self.move(x, y)  # 移动self.popup_window的位置，通过改x，y的值
        self.list_name = []

    def list_item(self, event):
        if event.checkState():
            self.list_name.append(event.text())


    def send(self):
        print "sen"
        self.world.my_signal.emit(self.list_name)

    def close1(self):
        self.close()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    b = main_view()
    b.show()
    app.exec_()


