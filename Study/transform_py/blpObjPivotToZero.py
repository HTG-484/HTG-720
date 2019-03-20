import maya.cmds as cmds
import maya.mel as mel

def osbGetRunOnAllObjects():
    return 1
#	 return menuItem("-q", "-checkBox", "osbRunOnAllGeoCB");

def blpObjPivotToZero():
	sl = []
	if (osbGetRunOnAllObjects()):
		sl = cmds.ls(exactType="transform")
		cmds.select(cl=1)
	else:
		sl = cmds.ls(sl=1)
		cmds.select(cl=1)

	defItems = ["persp", "front", "side", "top"]
	checkList = [i for i in sl if i not in defItems]  # 求列表ls与列表defItems的差集
	defMatrix = [0, 0, 0]
	for s in checkList:

		diff_num = 0
		scale_piv = cmds.xform(s,q=1,scale=1)
		rotate_piv = cmds.xform(s,q=1, rotation=1)

		for i in range(len(defMatrix)):	
			if (scale_piv[i] != defMatrix[i] and rotate_piv[i] != defMatrix[i]):    
				diff_num = diff_num + 1
		if (diff_num > 0):
			cmds.select(s,add=1)
def blpObjPivotToZeroFix():

	list = cmds.ls(sl=1)
	for s in list:
		cmds.move(0,0,0, s + ".scalePivot", s + ".rotatePivot")
blpObjPivotToZero()
blpObjPivotToZeroFix()


    
    
