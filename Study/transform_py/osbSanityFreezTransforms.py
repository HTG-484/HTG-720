import maya.cmds as cmds
import maya.mel as mel

def osbGetRunOnAllObjects():
        return (mel.eval('menuItem("-q", "-checkBox", "osbRunOnAllGeoCB");'))

def osbSanityFreezTransforms():
    if osbGetRunOnAllObjects():
        selectlist = cmds.ls(exactType="transform")
        cmds.select(cl=True)
    else:
        selectlist = cmds.ls(sl=1)
        cmds.select(cl=True)

    for s in selectlist:
        cmds.makeIdentity(s, apply=True, t=1, r=1, s=1, n=0)
