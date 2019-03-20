# -*- coding: utf-8 -*-
import re
import maya.cmds as cmds
'''命名规则要正确,已更改shape节点名称的更改不了'''
def conbin_name():
    shapeName = cmds.ls(dag = 1,type = 'shape')
    Defult = ['perspShape','topShape','frontShape','sideShape']
    shapeName = [i for i in shapeName if i not in Defult]
    Shapelist = []
    #finsh_conbin_name = []
    match = re.compile(r'\w*Shape\w*')
    for i in shapeName:
        Shapelist.append(match.findall(i))
    Shapelist = [i for i in Shapelist if len(i)==1]
    for i in Shapelist:
        cmds.rename(i[0],i[0].split('Shape')[0]+i[0].split('Shape')[1]+'Shape')
        #a,b = i[0].split('Shape')
        #finsh_conbin_name.append(a + b + 'Shape')
    #return finsh_conbin_name
conbin_name()
