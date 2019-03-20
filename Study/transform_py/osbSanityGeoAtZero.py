import maya.cmds as cmds
import maya.mel as mel

def osbGetRunOnAllObjects():
    pass
#    return 1
#	return mel.eval('menuItem("-q", "-checkBox", "osbRunOnAllGeoCB");')
	
def getMesh(obj):
    type = cmds.objectType(obj)
    if type == "mesh":
        return obj
    elif type == "transform":
        shapes=cmds.listRelatives(obj,type = "mesh" )
        return shapes[0]
	cmds.error("Don't get here")
	
def getMeshesFromSelection():
	sl = cmds.ls(sl=1)
	meshes=[]
	for s in sl:
		meshes.append(getMesh(s))
	return meshes

def getObjectsBasedOnPrefs():
	if osbGetRunOnAllObjects():
		sl = cmds.ls(exactType = "mesh")
	else:
		sl = getMeshesFromSelection()
	return sl
#�Ƿ��м���������洩��
def osbSanityGeoAtZero():
    obj = []
    sl=getObjectsBasedOnPrefs()
    for s in sl:
        bb=cmds.polyEvaluate(s, b=1)
        if bb[1][0]<-0.005:
            obj.append(s)
    cmds.select(obj)
    
#���Դ���
#sl = cmds.ls(exactType = "mesh")
#for s in sl:
#    bb=cmds.polyEvaluate(sl, b=1)
#    if bb[1][0]<-0.005:
#        cmds.select(sl)    
    

