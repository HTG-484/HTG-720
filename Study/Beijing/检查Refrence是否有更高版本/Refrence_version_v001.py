#!/usr/bin/env python
# -*- coding:utf-8 -*-
#文件命名规范为 eg.v001  请注意字母大小写.

import os
import re
import sys
import maya.cmds as cmds
import maya.mel as mel

'''得到refrence信息'''

def getAllReferences():
    '''2018.01.18 change '''
    result = []
    allRN = cmds.ls(rf=True)

    if 'sharedReferenceNode' in allRN:
        allRN.remove('sharedReferenceNode')
    for rn in allRN:
        # print "rn:",rn
        refPath = cmds.referenceQuery(rn, filename=True)
        namespace = cmds.referenceQuery(rn, namespace=True)
        if namespace[0] == ':':
            namespace = namespace[0:]

        info = {'node': rn,
                'ref_path': refPath,
                'path': refPath,
                'name': rn,
                'namespace': namespace
                }
        result.append(info)
    return result

'''得到当前renfrence版本路径'''

def get_dir_path():
    refrencePath = []
    version_info = []
    pathList = []
    refrence_info = getAllReferences()
    for i in refrence_info:
        refrencePath.append(i['path'])
    for i in refrencePath:
        version_info.append(i.split('/')[:-2])
    for i in range(len(version_info)):
        pathList.append('/'.join(version_info[i]))
    return pathList

'''返回存在最新版本文件路径'''

def get_up_refrenceversion():
    refrence_info = getAllReferences()
    #print refrence_info
    path = get_dir_path()
    #print path
    last_path = []
    for j in range(len(refrence_info)):
        try:
            if int(os.listdir(path[j])[-1].split('v')[1]) > int(refrence_info[j]['path'].split('/')[-2].split('v')[1]):
                last_path.append(path[j] + '/' + os.listdir(path[j])[-1])
        except:
            print u"请检查文件命名是否有误！！！"
        else:
            if int(os.listdir(path[j])[-1].split('v')[1]) > int(refrence_info[j]['path'].split('/')[-2].split('v')[1]):
                last_path.append(path[j] + '/' + os.listdir(path[j])[-1])
    if len(last_path)>0:
        print u"有最新版本存在路径为：",list(set(last_path))
    return list(set(last_path))


print get_up_refrenceversion()


