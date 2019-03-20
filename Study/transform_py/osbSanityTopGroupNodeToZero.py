import maya.cmds as cmds
import maya.mel as mel


# Place top group node pivot to world 0
def osbSanityTopGroupNodeToZero():

	# get all transforms that don't have any parents

	trans = cmds.ls(exactType="transform")
	topLevel=[]
	for s in trans:
		if (getParents(s) == 0 and s != "top" and s != "side"  and s != "front" and s != "persp"):
			topLevel.append(s)
	print topLevel		
	# there can be only one
	if (len(topLevel) > 1):
		cmds.confirmDialog(title='Top Level Nodes',message=u'警告根据规范每个资产元素顶层应该只有一个组',button="OK")
	if (len(topLevel) == 1):
		cmds.move(0,0,0,topLevel[0]+".scalePivot",topLevel[0]+".rotatePivot")
def getParents(obj):
	relatives = cmds.listRelatives(obj , parent = 1 , f=1 )
#	return relatives
	if relatives == None:
	    return 0

getParents('pSphere1')
osbSanityTopGroupNodeToZero()
