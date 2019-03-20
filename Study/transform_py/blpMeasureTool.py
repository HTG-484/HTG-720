import maya.cmds as cmds


def getParents(a):
    relatives = cmds.listRelatives(a, parent=True, f=True)  # 这个命令列出DAG对象的父母#f 返回完整的路径名#p 返回父节点
    if relatives == None:
        return 0
    else:
        return 1


def blpMeasureTool():
    trans = cmds.ls(et="transform")
    topLevel = []
    a = 1
    for s in trans:
        if (s == 'measureTool_blp'):
            cmds.delete('measureTool_blp')
        elif (getParents(s) == 0 and s != 'top' and s != 'side' and s != 'front' and s != 'persp'):
            topLevel.append(s)
    if len(topLevel) > 1:
        cmds.confirmDialog(title='Top Level Nodes', message=u'警告根据规范每个资产元素顶层应该只有一个组', button='OK')
    if len(topLevel) == 1:
        topObj = topLevel[0]
        pivs = cmds.xform(topObj, q=True, ws=True, piv=True)
        piv = []
        piv_0 = (pivs[0] + pivs[3]) / 2.0
        piv.append(piv_0)
        piv_1 = (pivs[1] + pivs[4]) / 2.0
        piv.append(piv_1)
        piv_2 = (pivs[2] + pivs[5]) / 2.0
        piv.append(piv_2)
        cube = cmds.polyCube()  # 多维数据集命令创建一个新的多边形立方体。
        cmds.connectAttr((topObj + '.boundingBox.boundingBoxSize'), (cube[0] + '.scale'))  # 连接两个依赖节点的属性并返回两个连接属性的名称
        cmds.move(piv[0], piv[1], piv[2], cube[0], ws=True)
        scaleY = cmds.getAttr(cube[0] + '.scaleY')
        measures = cmds.distanceDimension(sp=(0, 0, 0), ep=(0, scaleY, 0))  # 这个命令是用来创建一个距离维度来显示两个指定点之间的距离。
        locs = cmds.listConnections(measures)  # 这个命令返回一个列表的所有属性/指定类型的对象连接到给定对象
        goupName = cmds.group(measures, locs, n='measureTool_blp')  # 这个命令组指定的对象在一个新的组,并返回新组的名称
        cmds.delete(cube)


blpMeasureTool()
