# -*- coding:utf-8 -*-
import sys
import maya.cmds as cmds
from renderUI import RenderUI
class RenderApi(RenderUI):
    def __init__(self,parent=None):
        RenderApi.__init__(self,parent)
    def startProgress(self):
        pass
window=RenderApi()
window.show()
