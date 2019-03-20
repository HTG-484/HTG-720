# -*- coding: utf-8 -*-
import maya.cmds as cmds

objName = cmds.ls( dag=1, type=['mesh','nurbsSurface'])
myTransformNodes = cmds.listRelatives( objName, p= True)
shapes = cmds.ls(dag = 1,type = 'shape')
Defult = ['perspShape','topShape','frontShape','sideShape']
shapeName = [i for i in shapes if i not in Defult]
for i in range(len(myTransformNodes)):
    cmds.rename(shapeName[i],myTransformNodes[i]+'Shape')
