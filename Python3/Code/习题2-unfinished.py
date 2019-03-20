'''
练习题2：
用QT Designer设计一个用户登录界面（包含用户名和密码）
然后使用PyUIC将.ui文件转换为.py文件，并编写相应python代码
点击 ‘登陆’按钮，可以验证用户输入的用户名和密码
然后通过消息盒子提示用户密码是否输入错误，点击‘取消’按钮关闭登录窗口
用户名和密码可以硬编码在程序中
'''
import sys
import Login
from  PySide2.QtWidgets import QApplication,QMainWindow,QMessageBox