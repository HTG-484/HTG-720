import maya.cmds as cmds

cmds.render()

cam = cmds.camera()
cmds.render( cam[0], x=768, y=576 )