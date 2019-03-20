# -*- coding: utf-8 -*-
import maya.cmds as cmds

def Batch_eidt_shape_name():
    
    Defult = ['perspShape','topShape','frontShape','sideShape']
    objName = cmds.ls( dag=1, type=['mesh','nurbsSurface','locator','camera'])
    shapeNodes = [i for i in objName if i not in Defult]
    #objName = [i for i in objName if i not in Defult]
    TransformNodes = cmds.listRelatives( shapeNodes, p= True)
    cmds.select(TransformNodes)
    for i in range(len(TransformNodes)):
        cmds.rename(shapeNodes[i],TransformNodes[i]+'Shape')
    return cmds.ls(dag = 1,type = 'shape',v = 1)
