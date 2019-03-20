# -*- coding: utf-8 -*-
import maya.cmds as cmds

Defult = ['perspShape','topShape','frontShape','sideShape']
objName = cmds.ls( dag=1, type=['mesh','nurbsSurface','locator','camera'])
objNames = [i for i in objName if i not in Defult]
#objName = [i for i in objName if i not in Defult]
myTransformNodes = cmds.listRelatives( objNames, p= True)
shapes = cmds.ls(dag = 1,type = 'shape')
shapeName = [i for i in shapes if i not in Defult]
for i in range(len(myTransformNodes)):
    cmds.rename(shapeName[i],myTransformNodes[i]+'Shape')
