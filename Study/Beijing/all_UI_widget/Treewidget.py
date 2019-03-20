#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
try:
    from PySide2 import QtWidgets
    from PySide2 import QtCore
except ImportError:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore


class TreeWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)
        self.resize(500,400)
        self.setWindowTitle('TreeWidget')

        self.intUI()

    def intUI(self):
        self.tree = QtWidgets.QTreeWidget(self)
        comboBox = QtWidgets.QComboBox(self)
        comboBox.addItem('1')
        comboBox.addItem('2')
        self.tree.setColumnCount(5)
        self.tree.setHeaderLabels(['Key', 'Value'])
        root = QtWidgets.QTreeWidgetItem(self.tree)
        root.setText(0, 'root')
        child1 = QtWidgets.QTreeWidgetItem(root)
        child1.setText(0, 'child1')
        child1.setText(1, 'name1')
        child2 = QtWidgets.QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, 'name2')
        child3 = QtWidgets.QTreeWidgetItem(root)
        child3.setText(0, 'child3')
        child4 = QtWidgets.QTreeWidgetItem(child3)
        child4.setText(0, 'child4')
        child4.setText(1, 'name4')

        self.tree.setItemWidget(child1, 1, comboBox)
        self.tree.addTopLevelItem(root)
        self.setCentralWidget(self.tree)
        comboBox.currentIndexChanged.connect(self.change)

    def change(self):
        print 'a'

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tp = TreeWidget()
    tp.show()
    app.exec_()
