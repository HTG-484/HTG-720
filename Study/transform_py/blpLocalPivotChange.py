import maya.cmds as cmds

import maya.mel as mel

def osbGetRunOnAllObjects():
	return 1

def blpLocalPivotChange():
	if (osbGetRunOnAllObjects()):
		sl=cmds.ls(et="transform")
		cmds.select(clear=True)
	else:
		sl=cmds.ls(sl=True)
		cmds.select(clear=True)
	defItem=['persp','front','side','top']
	checkList=ret = list(set(defItem) ^ set(sl))
	defMatrix=[0,0,0]
	noZeroList=[]
	pre=0.00001
	for s in checkList:
		diff_num=0
		scale_piv=cmds.xform(s,q=True,scalePivot=True)
		rotate_piv=cmds.xform(s,q=True,rotatePivot=True)
		for i in range(len(defMatrix)):
			if (scale_piv[i]!=defMatrix[i] or rotate_piv[i]!=defMatrix[i]):
				diff_num=diff_num+1
		if diff_num>0:
			noZeroList.append(s)
	for t in noZeroList:
		obj_diff_num=0
		obj_scale_piv=cmds.getAttr(t+'.scalePivot')[0]
		obj_rotate_piv=cmds.getAttr(t+'.rotatePivot')[0]
		bb_matrix=cmds.objectCenter(t,l=True)
		for n in range(len(bb_matrix)):
			if (obj_scale_piv[n] - bb_matrix[n] < 0 - pre or obj_scale_piv[n] - bb_matrix[n] > 0 + pre or obj_rotate_piv[n] - bb_matrix[n] < 0 - pre or obj_rotate_piv[n] - bb_matrix[n] > 0 + pre):
				obj_diff_num=obj_diff_num+1
		if obj_diff_num>0:
			cmds.select(t,add=True)
def blpLocalPivotChangeFix():
	ls=cmds.ls(sl=True)
	for s in ls:
		cmds.xform(s,cp=True)

blpLocalPivotChange_main()
