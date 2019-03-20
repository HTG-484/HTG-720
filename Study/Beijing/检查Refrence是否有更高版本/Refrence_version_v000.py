#!/usr/bin/env python
# -*- coding:utf-8 -*-

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


'''得到文件夹下面的子文件夹名称'''

def get_dirs_name(path):
    dir_name = []
    for i in os.listdir(path):
        dir_name.append(i)
    return dir_name

def get_up_refrenceversion():
    refrence_info = getAllReferences()
    path = get_dir_path()
    # int(refrence_info[1]['path'].split('/')[-2].split('v')[1])
    last_path = []
    for j in range(len(refrence_info)):
        if int(os.listdir(path[j])[-1].split('v')[1]) > int(refrence_info[j]['path'].split('/')[-2].split('v')[1]):
            last_path.append(path[j] + '/' + os.listdir(path[j])[-1])
    return last_path


get_up_refrenceversion()


