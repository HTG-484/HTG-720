# -*- coding:utf-8 -*-
from PySide import QtGui,QtCore
import sys

class Window(QtGui.QDialog):
    def __init__(self,parent = None):
        super(Window, self).__init__(parent)
        self.resize(700,600)
        self.initUI()
        self.rightfunction()
    def initUI(self):
        self.tablewidget = QtGui.QTableWidget()
        self.tablewidget.horizontalHeader().setDefaultSectionSize(150)#设置列宽度
        self.tablewidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)#自适应行宽
        self.tablewidget.verticalHeader().setDefaultSectionSize(40)
        #self.tablewidget.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        header = ['1','2','3','4','5']
        self.tablewidget.setHorizontalHeaderLabels(header)
        self.tablewidget.setColumnCount(5)#   //设置行数和列数
        self.tablewidget.setRowCount(10)
        font = QtGui.QFont() #   //表头字体加粗
        font.setBold(True)
        self.tablewidget.horizontalHeader().setFont(font)
        self.tablewidget.setFrameShape(QtGui.QFrame.NoFrame)#   //设置无边框
        #self.tablewidget.setShowGrid(False)#   //设置不显示格子线
        self.tablewidget.verticalHeader().setVisible(True)#   //设置垂直头不可见

        #self.tablewidget.setSelectionBehavior(QtGui.QAbstractItemView.ExtendedSelection)#   //可多选（Ctrl、Shift、Ctrl+A都可以）
        #self.tablewidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)#  //设置选择行为时每次选择一行
        self.tablewidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)#   //设置不可编辑
        self.tablewidget.horizontalHeader().resizeSection(0, 150)#  // 设置表头第一列的宽度为150
        self.tablewidget.horizontalHeader().setFixedHeight(25)#    //设置表头的高度
        self.tablewidget.setStyleSheet("selection-background-color:lightblue;")#  //设置选中背景色
        self.tablewidget.horizontalHeader().setStyleSheet("QHeaderView::section{background:LightSteelBlue;}")#   //设置表头背景色
        #  //设置水平、垂直滚动条样式
        self.tablewidget.horizontalScrollBar().setStyleSheet("QScrollBar{background:transparent; height:10px;}"
        "QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}"
        "QScrollBar::handle:hover{background:gray;}"
        "QScrollBar::sub-line{background:transparent;}"
        "QScrollBar::add-line{background:transparent;}")

        self.tablewidget.verticalScrollBar().setStyleSheet("QScrollBar{background:transparent; width: 10px;}"
        "QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}"
        "QScrollBar::handle:hover{background:gray;}"
        "QScrollBar::sub-line{background:transparent;}"
        "QScrollBar::add-line{background:transparent;}")

        self.tablewidget.setItemDelegate(NoFocusDelegate())  #去除选中的iteam有虚框
        self.tablewidget.horizontalHeader().setHighlightSections(False) #  //点击表时不对表头行光亮（获取焦点）

        self.progressBar = QtGui.QProgressBar()
        self.startBtn = QtGui.QPushButton('Start')
        self.hLay = QtGui.QHBoxLayout()
        self.hLay.addWidget(self.progressBar)
        self.hLay.addWidget(self.startBtn)
        self.lay = QtGui.QVBoxLayout()
        self.lay.addWidget(self.tablewidget)
        self.lay.addLayout(self.hLay)
        self.setLayout(self.lay)

        new = QtGui.QTableWidgetItem('aaa')
        self.tablewidget.setItem(0,0,new)


        self.tablewidget.cellDoubleClicked.connect(self.edit)
        self.startBtn.clicked.connect(self.start)

    def start(self):
        number = 100
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(number)

        for i in range(number):
            self.progressBar.setValue(i+1)
            QtCore.QThread.msleep(10)
        else:
            pass






    def edit(self):
        row = self.tablewidget.currentRow()
        column = self.tablewidget.currentColumn()
        self.editRow(row,column)

    def editRow(self,edit_row,edit_column):
        item = self.tablewidget.item(edit_row,edit_column)
        self.tablewidget.setCurrentCell(edit_row,edit_column)
        self.tablewidget.openPersistentEditor(item)
        self.tablewidget.editItem(item)
        #self.tablewidget.closeEditor(item)#  //关闭编辑项

    def insertItem(self):
        row_count = self.tablewidget.rowCount()#  //获取总行数
        self.tablewidget.insertRow(row_count)
        self.tablewidget.setItem()
        self.tablewidget.setItem(row_count,0,)


    def rightfunction(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)######允许右键产生子菜单
        self.customContextMenuRequested.connect(self.showContextMenu)####右键菜单
        self.contextMenu = QtGui.QMenu()  #   //创建QMenu
        self.actionA = self.contextMenu.addAction(u'功能一')
        self.actionB = self.contextMenu.addAction(u'功能二')
        self.actionA.triggered.connect(self.CopyFile)
        self.actionB.triggered.connect(self.functionB)

    def showContextMenu(self, pos):
        print pos
        if self.tablewidget.currentColumn() == 2:
            self.contextMenu.move(self.pos() + pos)  # 菜单显示前，将它移动到鼠标点击的位置
            self.contextMenu.show()

    def CopyFile(self):
        clip_path = []
        clip_data = []
        for i in range(len(self.tablewidget.selectedIndexes())):
            path = self.tablewidget.selectedItems()[i].text()
            clip_path.append(path)
        clip_board = QtGui.QApplication.clipboard()
        data = QtCore.QMimeData()
        for i in clip_path:
            getUrl = QtCore.QUrl.fromLocalFile(i)
            clip_data.append(getUrl)
        data.setUrls(clip_data)
        clip_board.setMimeData(data)

    def functionB(self):
        pass

    def get_row_toScrollbar(self,text):
        item = self.tableWidget.findItems(text, QtCore.Qt.MatchExactly)#遍历表查找对应的item
        row = item[0].row()                                            #获取其行号
        self.tableWidget.verticalScrollBar().setSliderPosition(row)  #滚轮定位过去，搞定


        self.tablewidget.setItemDelegate(NoFocusDelegate())  #去除选中的iteam有虚框
#去虚框的方法
class NoFocusDelegate(QtGui.QStyledItemDelegate):
    def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
        if (QStyleOptionViewItem.state & QtGui.QStyle.State_HasFocus):
            QStyleOptionViewItem.state = QStyleOptionViewItem.state^QtGui.QStyle.State_HasFocus
        QtGui.QStyledItemDelegate.paint(self,QPainter, QStyleOptionViewItem, QModelIndex)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    qw = Window()
    qw.show()
    app.exec_()

