import maya.cmds as cmds
import maya.mel as mel

def osbGetRunOnAllObjects():
    return 1


#	 return menuItem("-q", "-checkBox", "osbRunOnAllGeoCB");

def blpTransformChange():
    sl = []
    checkList = []

    if (osbGetRunOnAllObjects()):
        sl = cmds.ls(exactType="transform")
        cmds.select(cl=1)
    else:
        sl = cmds.ls(sl=1)
        cmds.select(cl=1)

    defItems = ["persp", "front", "side", "top"]
    checkList = [i for i in sl if i not in defItems]  # 求列表ls与列表defItems的差集
    defMatrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

    for s in checkList:
        diff_num = 0
        matrix = cmds.getAttr(s + ".matrix")  # 返回所有的位置坐标

        for i in range(len(defMatrix)):

            if (matrix[i] != defMatrix[i]):
                diff_num = diff_num + 1

        if (diff_num > 0):
            cmds.select(s, add=1)


def blpTransformChangeFix():
    list = cmds.ls(sl=1)

    for s in list:
        cmds.makeIdentity(s, apply=True, t=1, r=1, s=1, n=0)

# blpTransformChange()
# blpTransformChangeFix()

