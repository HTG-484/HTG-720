#网格布局

#QGridLayout类  addWidget方法
#addSpacing
import sys
from PySide2.QtWidgets import QWidget,QLabel,QLineEdit,QTextEdit,QGridLayout,QApplication

class FormGridLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        #创建三个标签
        title=QLabel('标题')
        author=QLabel('作者')
        summary=QLabel('摘要')
        #创建三个文本输入框
        titleEdit=QLineEdit()
        authorEdit=QLineEdit()
        summaryEdit=QTextEdit()
        #创建网格布局对象
        grid=QGridLayout()
        #设置单元格的距离
        grid.setSpacing(10)
        #将创建的控件加入布局对象
        grid.addWidget(title,1,0)
        grid.addWidget(titleEdit,1,1)

        grid.addWidget(author,2,0)
        grid.addWidget(authorEdit,2,1)

        grid.addWidget(summary,3,0)
        grid.addWidget(summaryEdit,3,1,5,1)
        #把 布局应用于当前窗口
        self.setLayout(grid)

        self.setGeometry(300,300,350,300)

        self.setWindowTitle('网格布局')
        self.show()

if __name__=='__main__':
    app=QApplication(sys.argv)
    form=FormGridLayout()
    sys.exit(app.exec_())