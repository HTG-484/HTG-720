# -*- coding: utf-8 -*-
import maya.cmds as cmds
Allobj = cmds.ls(dag = 1,type = 'transform')
Defult = ['persp','top','front','side']
shapes = [i for i in Allobj if i not in Defult]
oneShape = []
moreShape = []
for i in shapes:
    children = cmds.listRelatives(i , children = True)
    if len(children) == 0:
        pass
    elif len(children) < 3:
        oneShape.append(i)
    else:
        moreShape.append(i)
print '这是三个shape节点的物体',oneShape
print '这是多个shape节点的物体',moreShape


