#!usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author:MCC
@file: findReferenceVersion
@time: 2018/07/18 17:30
"""
import os
import re
import sys
class FindReferenceVersion(object):
    def __init__(self):
        import maya.cmds as cmds
        import os
        self._cmds = cmds
        self._os = os

    def getAllReferences(self):
        '''2018.01.18 change '''
        result = []
        namespaceList = []
        referencePathList = []
        allRN = self._cmds.ls(rf=True)

        if 'sharedReferenceNode' in allRN:
            allRN.remove('sharedReferenceNode')
        for rn in allRN:
            refPath = self._cmds.referenceQuery(rn, filename=True)
            namespace = self._cmds.referenceQuery(rn, namespace=True)
            if namespace[0] == ':':
                namespace = namespace[0:]

            info = {'node': rn,
                    'ref_path': refPath,
                    'path': refPath,
                    'name': rn,
                    'namespace': namespace
                    }
            result.append(info)
        for ii in result:
            referencePathList.append(ii["ref_path"])
            namespaceList.append(ii["namespace"].split(":")[1])
        return list(set(referencePathList)),list(set(namespaceList))

    def getReferenceVersionNumsPath(self):  # 获得maya Reference版本号路径
        reList = []
        versionPath = []
        dict_all = {}
        versionDict = {}
        referencePath, referenceName = self.getAllReferences()
        for ii in xrange(len(referencePath)):
            detepat = re.compile("(v\d+)")
            result = detepat.finditer(referencePath[ii])
            for m in result:
                reList.append(m.group())
                versionPath.append(referencePath[ii].split("/%s" % (reList[ii]))[0])
        for ii in xrange(len(referencePath)):
            
            dict_all[referenceName[ii]] = versionPath[ii]
        for ii in xrange(len(reList)):
            versionDict[referenceName[ii]] = reList[ii]

        return dict_all, versionDict

    def getDirName(self):
        listDir = []
        lastDict = {}
        listDirFiles = []
        dict_all, versionDict = self.getReferenceVersionNumsPath()
        dict_key = dict_all.keys()
        for ii in dict_key:
            listDir.append(dict_all[ii])

        for ii in listDir:
            listDirFiles.append(os.listdir(ii))
        for ii in xrange(len(listDirFiles)):
            lastDict[dict_key[ii]] = max(listDirFiles[ii])

        return lastDict

    def compareVersion(self):
        versionListPath = []
        dict_all, versionDict = self.getReferenceVersionNumsPath()
        lastDict = self.getDirName()
        for key, value in versionDict.items():
            if versionDict[key] < lastDict[key]:
                fileNames = os.listdir("%s/%s" % (dict_all[key], lastDict[key]))
                if fileNames != []:
                    versionListPath.append("%s/%s/%s"%(dict_all[key], lastDict[key], fileNames[0]))       
        return versionListPath

findReferenceVersion = FindReferenceVersion()
print findReferenceVersion.compareVersion()
