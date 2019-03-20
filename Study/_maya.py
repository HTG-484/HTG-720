# -*- coding: utf-8 -*-

'''
This module contains common ed functions of Mayaus.
'''

import os
import json
import re
import pkmg
reload(pkmg)

fllb = pkmg.import_('file_lib')
reload(fllb)


class Maya(object):
    def __init__(self):
        import maya.cmds as cmds
        import maya.mel as mel
        import pymel.core as pm
        self._pm = pm
        self._mel = mel
        self._cmds = cmds
    
    def app(self):
        return 'maya'
    
    def extension(self):
        return self.extensions()[0]
    
    def extensions(self):
        return ['ma', 'mb']
    
    
    #---------------------------------- Basic Parameters -------------------------------
    
    _fpsMap = {
        'game': 15,
        'film': 24,
        'pal': 25,
        'ntsc': 30,
        'show': 48,
        'palf': 50,
        'ntscf': 60,
    }
    def fps(self): 
        r = self._cmds.currentUnit(fullName=True, query=True, time=True)
        return self._fpsMap.get(r)
    
    def setFps(self, value):
        self._cmds.currentUnit(time=value)
    
    def resolution(self):
        width = self._cmds.getAttr('defaultResolution.width')
        height = self._cmds.getAttr('defaultResolution.height')
        return width,height
    
    def currentFrame(self):
        return self._cmds.currentTime(query=True)
    
    def frameRange(self):
        minT = self._cmds.playbackOptions(query=True, minTime=True)
        maxT = self._cmds.playbackOptions(query=True, maxTime=True)
        return [minT, maxT]
    
    def setFrameRange(self, firstFrame, lastFrame):
        self._cmds.playbackOptions(minTime=firstFrame,
                                   maxTime=lastFrame,
                             animationStartTime=firstFrame,
                             animationEndTime=lastFrame)
    
    def filename(self):
        filename = os.path.basename(self.filepath())
        return filename
    
    def filepath(self):
        return self._cmds.file(query=True, location=True)
    
    def fileType(self, path=''):
        if not path:
            path = self.filepath()
        
        exts = {
            'ma': 'mayaAscii',
            'mb': 'mayaBinary',
        }
        ext = os.path.splitext(path)[1].replace('.','')
        if exts.has_key(ext):
            typ = exts[ext]
        else:
            typ = ''
        return typ
    
    def hasUnsavedChanges(self):
        '''Checks whether or not there're unsaved changes.'''
        if self._cmds.file(query=True, modified=True):
            return True #have change and don't save
        else:
            return False

    def isUntitled(self):
        '''Checks whether or not the current file is untitled.'''
        if self.filename() == 'unknown':
            return True
        else:
            return False
    
    def sceneUnit(self):
        '''Gets the linear unit of the current scene.'''
        #self._cmds.currentUnit(fullName=True, query=True, linear=True)
        #self._cmds.currentUnit(fullName=True, query=True, angle=True)
        #self._cmds.currentUnit(fullName=True, query=True, time=True)
        #self._cmds.currentUnit(time='ntsc')
        #self._cmds.currentUnit(angle='degree')
        #self._cmds.currentUnit(linear='in')
        return self._cmds.currentUnit(fullName=True, query=True, linear=True)
    
    def setSceneUnit(self, value):
        '''
 	Sets the current linear unit. Valid strings are:
            [mm | millimeter | cm | centimeter | m | meter | km | kilometer |
             in | inch | ft | foot | yd | yard | mi | mile] 
        '''
        self._cmds.currentUnit(linear=value)
    
    
    
    #---------------------------------- Input and Output -------------------------------
    
    def new(self, force=False):
        self._cmds.file(force=force, newFile=True, prompt=False)
        return True
    
    def open(self, path, force=False):
        self._cmds.file(path, force=force, open=True, prompt=False)
        return True
    
    def save(self, force=False, type=''):
        if type:
            self._cmds.file(force=force, save=True, prompt=False, type=type)
        else:
            self._cmds.file(force=force, save=True, prompt=False)
        
        return True
    
    def saveAs(self, path, force=False):
        self._cmds.file(rename=path)
        
        typ = self.fileType(path)
        if typ:
            self.save(force=force, type=typ)
        else:
            self.save(force=force)
        return True
    
    def close(self):
        pass
    
    def exit(self):
        pass
    
    def getSceneHierarchy(self):
        all  = self._cmds.ls(type="transform")
        other = ["front","persp","side","top"]
        for i in other:
            all.remove(i)
        parentHierarchy = []
        for i in all:
            A = self._cmds.listRelatives(i,p=1)
            if A ==None:#get all parent hierarchy
                parentHierarchy.append(i)
        return parentHierarchy
    
    def mergeImport(self, path):
        def changeHierarchy(oldH,newH):
            newLay = self._cmds.listRelatives(newH,c = 1)
            oldLay = self._cmds.listRelatives(oldH,c = 1)
            #print newLay,oldLay,"_____________________"
            for nlay in newLay:
                nlay2 = nlay[(nlay.index(":")+1):]
                #print "nlay:",nlay
                if nlay2 in oldLay:
                    oldH2 = oldH+"|"+nlay2
                    newH2 = newH+"|"+nlay
                    if self._cmds.nodeType(newH2) != "mesh":
                        #print newH2
                        changeHierarchy(oldH2,newH2) 
                    else:
                        root = self._pm.PyNode(newH2)
                        A = root.listRelatives(ap=True)
                        objectName = A[0].longName()
                        #print objectName
                        rootHierar = self._pm.PyNode(oldH2)
                        B = rootHierar.listRelatives(ap=True)
                        shape = B[0].longName()
                        shapeList = shape.split("|")
                        moveHierarchy = ""  
                        for hiera in shapeList:
                            if hiera != "":
                                if hiera != shapeList[-1]:
                                    moveHierarchy = moveHierarchy+"|"+hiera
                                    
                        #print objectName,"-->",moveHierarchy
                        self._cmds.parent(objectName,moveHierarchy)
                        oldName = objectName.split("|")[-1]
                        newName = oldName.split(":")[-1]
                        self._cmds.rename(oldName,newName)
                else:
                    #print nlay,"-->",oldH
                    self._cmds.parent(nlay,oldH)
                    oldName = nlay.split("|")[-1]
                    newName = oldName.split(":")[-1]
                    self._cmds.rename(oldName,newName)
                    listChild = self._cmds.listRelatives(newName,ad=1)
                    for child in listChild:
                        newChild = child.split(":")[-1]
                        try:
                            self._cmds.rename(child,newChild)
                        except:
                            pass
        
        oldH = self.getSceneHierarchy()
        
        newNamespace = self.normalImport(path)
        
        newH = self.getSceneHierarchy() 
        
        for i in oldH:
            newH.remove(i)
        
        #print oldH,newH
        
        result = []
        for new in newH:
            # a1
            if ":" in new:
                lenN = (new.index(":")+1)
                new2 = new[lenN:]
                if new2 in oldH:
                    #print [new2],[new]
                    oldHierar = new2
                    newHierar = new
                    changeHierarchy(oldHierar,newHierar)
                    
                    result.append(new)
                    self._cmds.delete(new)
        
        if result == []:
            self.removeObjectNamespaces(newNamespace)
        
        return result
    
    def normalImport(self, path, removeNamespace=False):
        oldNamespaces = self._cmds.namespaceInfo(lon=True)
        
        self._cmds.file(path, i=True, namespace='')
        
        newNamespaces = self._cmds.namespaceInfo(lon=True)
        for old in oldNamespaces:
            newNamespaces.remove(old)
        
        if newNamespaces:
            namespace = newNamespaces[0]
            
            if removeNamespace:
                self.removeObjectNamespaces(namespace)
                namespace = ''
        
        else:
            namespace = ''
        
        return namespace
    
    def import_(self, path, removeNamespace=False):
        oldH = self.getSceneHierarchy()
        
        if oldH:
            if removeNamespace:
                option = 'merge'
            else:
                option = 'normal'
        else:
            option = 'normal'
        
        if option == 'merge':
            #print 'merge'
            self.mergeImport(path)
            namespace = ''
        
        else:
            print 'normal'
            namespace = self.normalImport(path, removeNamespace)
        
        info = {
            'namespace': namespace.lstrip(':'),
            'path': path
        }
        return info
    
    def importAbc(self, path):
        self._cmds.AbcImport(path, mode=True)
        return True
    
    def exportFbx(self, path):
        self._cmds.file(path, force=True,
                        options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1",
                        type="FBX export", pr=True, ea=True)
    
    def exportAbc(self, path, frameRange=None, objects=[]):
        '''fr is list [0,1]'''
        #AbcExport -j "-frameRange 1 34 -dataFormat ogawa -root |camera:tst_001_01 -root |dog:dog -file C:/Users/nian/Documents/maya/projects/default/cache/alembic/test.abc";
        
        # Get arguments
        if frameRange == None:
            frameRange = self.frameRange()
        
        #print frameRange
        args = '-frameRange %s %s ' % (frameRange[0], frameRange[1])
        args += '-stripNamespaces -uvWrite -worldSpace '
        args += '-dataFormat ogawa '
        
        for obj in objects:
            args += '-root %s ' % obj
        
        args += '-file %s' % path
        
        # Get cmd
        cmd = 'AbcExport -j "%s";' % args
        
        self._pm.mel.eval(cmd)
    
    def exportSelected(self, path):
        typ = self.fileType(path)
        if typ:
            self._cmds.file(path, force=True, exportSelected=True, typ=typ)
        else:
            self._cmds.file(path, force=True, exportSelected=True)
    
    def reference(self, path):
        filename = os.path.basename(path)
        namespace = os.path.splitext(filename)[0]
        p = self._cmds.file(path, reference=True, namespace=namespace)
        node = self._cmds.referenceQuery(p, referenceNode=True)
        namespace = self._cmds.referenceQuery(p, namespace=True)
        #print namespace
        info = {
            'node': node,
            'namespace': namespace.lstrip(':'),
            'ref_path': p,
            'path': path
        }
        return info
    
    def removeReference(self, refPath):
        self._cmds.file(refPath, removeReference=True)
    
    def getReferences(self):
        result = []
        allRe = self._cmds.ls(references=True)
        if allRe:
            for rn in allRe:
                refPath = self._cmds.referenceQuery(rn, filename=True)
                #print f
                if "{" in refPath:
                    path = refPath[:refPath.index("{")]
                else:
                    path = refPath
                
                namespace = self._cmds.referenceQuery(rn, namespace=True)
                
                info = {
                    'node': rn,
                    'ref_path': refPath,
                    'path': path,
                    'name': rn,
                    'namespace': namespace.replace(':',''),
                }
                result.append(info)
        
        return result
    
    def changeReference_bak1(self, path, loadReference):
        '''loadReference is nameSpace'''
        allRe = self._cmds.ls(references=True)
        if allRe:
            for rn in allRe:
                f = self._cmds.referenceQuery(rn, ns=True)
                #print f,RN
                getRef = ":%s"%loadReference
                if f == getRef:
                    #print rn
                    self._cmds.file(path,loadReference=rn,options="v=0")
    
    def setReferencePath(self, ref, path):
        '''Sets the reference path to a new path.'''
        self._cmds.file(path, loadReference=ref, options="v=0")
    
    def getReferenceObjects(self):
        rnHierarchy = []
        
        allObjectHierarchy = []
        all = self._cmds.ls(type="mesh")
        for i in all:
            root = self._pm.PyNode(i)
            A = root.listRelatives(ap=True)
            objectName = A[0].longName()
            #print objectName
            masterHierarchy = objectName.split("|")[1]  
            allObjectHierarchy.append(masterHierarchy)
        
        allRn = self._cmds.ls(type="reference")
        for j in allRn:
            try:
                referenceNode = self._cmds.referenceQuery(j,nodes=True)
                #print 'referenceNode:',referenceNode
                
                for r in referenceNode:
                    #print referenceNode[0]
                    if r in allObjectHierarchy:
                        rnHierarchy.append(r)
            
            except:
                #print j
                pass
        
        rnHierarchy = list(set(rnHierarchy))
        #print 'rnHierarchy:',rnHierarchy
        
        result = []
        for i in rnHierarchy:
            name = self.removeStringNamespace(i)
            info = {
                'name': name,
                'code': name,
                'full_name': i,
                'namespace': i.replace(name, '').replace(':','')
            }
            result.append(info)
        
        return result
    
    
    #---------------------------------- Geometry -------------------------------
    
    def select(self, path, replace=True, add=False, noExpand=False):
        if path and type(path) in (str, unicode):
            self._cmds.select(path, replace=replace, add=add,
                              noExpand=noExpand)
    
    def clearSelection(self):
        self._cmds.select(deselect=True)
    
    def delete(self, objects):
        self._cmds.delete(objects)
    
    def exists(self, path):
        if self._cmds.ls(path):
            return True
        else:
            return False
    
    def getSets(self, root=''):
        '''
        Gets scene sets created by the user.
        If root is not an empty string, it will only list the
        sets which has objects under the root node.
        
        Returns a dictionary where key is the set and value is
        a list of objects in it.
        Example:
            {u'Plastic': [u'|dog|base|pSphere1'],
             u'Wood': [u'|dog|base|pCone1'],
             u'set1': [u'|dog|proxy|pSphere2']
             }
        '''
        temp = self._cmds.ls(sets=True)
        sets = []
        for t in temp:
            if 'default' in t or 'initial' in t:
                pass
            else:
                sets.append(t)
        
        #print sets
        if root:
            if not root.startswith('|'):
                root = '|' + root
        
        #print 'root:',root
        
        result = {}
        for s in sets:
            info = []
            
            temp = self._cmds.sets(s, q=True)
            if temp:
                for t in temp:
                    objs = self._cmds.ls(t, long=True)
                    for obj in objs:
                        if root:
                            if obj.startswith(root):
                                info.append(obj)
                        else:
                            info.append(obj)
            
            if info:
                result[s] = info
        
        return result
    
    def createSets(self, sets, namespace=''):
        '''
        Creates scene sets.
        
        sets is a dictionary where key is the set and value is
        a list of objects in it.
        Example:
            {u'Plastic': [u'|dog|base|pSphere1'],
             u'Wood': [u'|dog|base|pCone1'],
             u'set1': [u'|dog|proxy|pSphere2']
             }
        '''
        allSets = self._cmds.ls(type="objectSet")
        defaultSet = [u'defaultLightSet', u'defaultObjectSet', u'initialParticleSE', u'initialShadingGroup']
        for i in defaultSet:
            allSets.remove(i)
        
        #print namespace
        #print allSets
        
        if sets:
            for s in sets.keys():
                objs = []
                
                for i in sets[s]:
                    if namespace:
                        i = self.addObjectNamespace(i, namespace)
                    if self.exists(i):
                        objs.append(i)
                s = self.addObjectNamespace(s, namespace)
                
                #print s
                
                if s not in allSets:
                    if objs:
                        self._cmds.sets(objs, name=s)
    
    def getChildren(self, path):
        nodes = self._pm.ls(path)
        if nodes:
            return nodes[0].getChildren()
        else:
            return []
    
    def getCameras(self):
        temp = self._cmds.ls(cameras=True, long=True)
        result = []
        for t in temp:
            if 'camera' in t:
                geo = '|'+t.split('|')[1]
                result.append(geo)
        return result
    
    def createHierachy_old(self, tree):
        '''
        tree: 
        {assetName:["proxy","base","contact",
                    "lod1","lod2","utility",
                    "paint","previse","symmetry"]
        }
        '''
        for asset in tree.keys():
            for group in tree[asset]:
                self._cmds.group(name=group, empty=True)
            
            self._cmds.group(tree[asset], name=asset)
    
    def checkHierachy_old(self, tree):
        '''Checks whether the hierachy of the scene matches the tree or not.'''
        for asset in tree.keys():
            for group in tree[asset]:
                geo = '|'.join([asset, group])
                #print 'geo:',geo
                if not self.exists(geo):
                    return False
        return True
    
    def checkHierachy_bak1(self,dic = {},ke="",errorList = []):
        a= "|"
        try:
            self._cmds.file(save=True)
        except:
            print u'当前文件没有保存'
        a= "|"
        for key in dic.keys():
            ke = ke+a+key
            #print ke
            if not self._pm.objExists(ke):
                errorList.append( u'文件层级名称不正确,%s层级不存在'%ke)
            #判断下一级是否还是字典，如果是字典继续递归
            if type(dic[key]) == type({}):
                #print dic[key]
                self.checkHierarchy(dic[key],ke,errorList)
            elif type(dic[key]) == type([]):
                for i in dic[key]:
                    err =  ke+"|"+i
                    if not self._pm.objExists(err):
                        errorList.append( u'文件层级名称不正确,%s层级不存在'%err)
            elif type(dic[key]) == type("wxcgtt"):
                err =  ke+"|"+dic[key]
                if not self._pm.objExists(err):
                    errorList.append( u'文件层级名称不正确,%s层级不存在'%err)
        
        #key = layer.keys()[0]
        #master = self._pm.objExists("|%s"%key)
        #if not master:
        #    errorList.append( u'文件层级名称不正确，根文件名称应该为%s'%key)
        
        #if not self._pm.sceneName():
        #    print u'当前文件没有保存'
        
        #lis = layer[key]
        #for Hie in lis:
        #    newHie = self._pm.objExists("|%s|%s"%(key,Hie))
        #    if not newHie:
        #        errorList.append(u"文件层级名称不正确，|%s下面需要有%s组"%(key,Hie))
        
        errorList = list(set(errorList))
        for i in errorList:
           F = i.encode("gbk")
        return errorList
    
    def createHierachy(self, dic={}):
        '''
        tree: 
        {assetName:["proxy","base","contact",
                    "lod1","lod2","utility",
                    "paint","previse","symmetry"]
        }
        '''
        def check(dic,root,errorList=[]):
            for key in dic.keys():
                _root = key
                _root = root+"|"+_root
                #print _root
                errorList.append(_root)
                if type(dic[key]) == list:
                    for ke in dic[key]:
                        #print _root+"|"+ke
                        errorList.append(_root+"|"+ke)
                elif type(dic[key])==dict:
                    check(dic[key],_root,errorList)
                else:
                    #print _root+"|"+dic[key]
                    errorList.append(_root+"|"+dic[key])
            return errorList
        ret = check(dic,"",[])
        
        for i in ret:
            if not self._cmds.objExists(i):
                groupname = i.split("|")[-1]
                parent = i.split("|")[-2]
                #print groupname,"Aaa"
                #print parent,"Bbb"
                #print i.split("|")
                
                if parent =="":
                    self._cmds.group(name = groupname,em=True)  
                else:
                    self._cmds.group(name = groupname,em=True,parent = parent)  
        return True
    
    def getExceptionObjects(self, tree):
        '''Gets objects which are not in the hierachy tree.'''
        def check(obj,newList):
            lay = self._cmds.listRelatives(obj,c=1)
            if lay != None:
                for la in lay:
                    try:
                        root = self._pm.PyNode(la)
                        longname = root.longName()
                        if self._cmds.nodeType(longname) != "mesh":
                            #mesh = self._cmds.listRelatives(longname,c=1)
                            #if self._cmds.nodeType(mesh) != "mesh" :  
                            #    newList.append(longname)
                            check(longname,newList)
                        else:
                            longN = self._cmds.listRelatives(longname,p=1)
                            root = self._pm.PyNode(longN[0])
                            longN = root.longName()
                            newList.append(longN)
                    
                    except:
                        pass
                
                if self._cmds.nodeType(lay) == "locator":
                    newList.append(obj)
        
        def getExcessObject(dic):
            all = self._cmds.ls(type="transform")
            view = ["persp","top","front","side"]
            for i in view:
                all.remove(i)
            
            lis = []
            for i in all:
                p =  self._cmds.listRelatives(i,p=1)
                if p == None:
                    lis.append(i)
            
            newLis= []        
            for i in lis:
                if i not in dic.keys():
                    root = self._pm.PyNode(i)
                    longname = root.longName()
                    #newLis.append(longname)
                    check(longname,newLis)
            return newLis
        
        return getExcessObject(tree)
    
    def checkHierachy(self, tree):
        '''Checks whether the hierachy of the scene matches the tree or not.'''
        errorL = []
        dic = tree
        def check(dic,root,errorList=[]):
            for key in dic.keys():
                _root = key
                _root = root+"|"+_root
                #print _root
                errorList.append(_root)
                if type(dic[key]) == list:
                    for ke in dic[key]:
                        #print _root+"|"+ke
                        errorList.append(_root+"|"+ke)
                elif type(dic[key])==dict:
                    check(dic[key],_root,errorList)
                else:
                    #print _root+"|"+dic[key]
                    errorList.append(_root+"|"+dic[key])
            return errorList
        
        ret = check(dic,"",[])
        
        for i in ret:
            if not self._cmds.objExists(i):
                err = u"%s组不存在" % i
                errorL.append(err)
        
        for i in self.getExceptionObjects(tree):
            err = u'%s不在层级中' % i
            errorL.append(err)
        
        return errorL
    
    def addExtraAttribute(self, objectName, attributeName, attributeValue, dataType='string'):
        '''Adds an extra attribute to the object.'''
        allAttributes = self._cmds.listAttr(objectName)
        if attributeName not in allAttributes:
            self._cmds.addAttr(objectName, shortName=attributeName, dataType=dataType)
        
        attrName = "%s.%s" % (objectName, attributeName)
        #print 'attrName:',attrName
        self._cmds.setAttr(attributeName, e=True, keyable=True)
        self._cmds.setAttr(attributeName, attributeValue, type=dataType)
    
    def removeObjectNamespaces(self, namespace):
        '''Removes namespaces of the scene objects.'''
        self._cmds.namespace(removeNamespace=namespace, mergeNamespaceWithParent=True)
    
    def removeStringNamespace(self, name):
        '''
        Removes namespaces of the name.
        For instance:
            name: |dog:dog|dog:base|dog:box|dog:boxShape
            return: |dog|base|box|boxShape
            
            name: |dog:box.f[10:13]
            return: |box.f[10:13]
        '''
        splitter = '|'
        
        pat = re.compile('[a-zA-Z0-9]+\.f\[\d+:\d+\]')
        
        split = name.split(splitter)
        temp = []
        for i in split:
            if i:
                # i: dog:box.f[10:13]
                find = pat.findall(i)
                if find:
                    new = find[-1]
                
                # Keep the last item
                else:
                    new = i.split(':')[-1]
            
            else:
                new = i
            
            temp.append(new)
        
        return splitter.join(temp)
    
    def addObjectNamespace(self, name, namespace):
        '''
        Adds namespaces to the name.
        For instance:
            name: |dog|base|box|boxShape
            namespace: dog
            return: |dog:dog|dog:base|dog:box|dog:boxShape
            
            name: |box.f[10:13]
            namespace: dog
            return: |dog:box.f[10:13]
        '''
        splitter = '|'
        
        pat = re.compile('[a-zA-Z0-9]+\.f\[\d+:\d+\]')
        
        split = name.split(splitter)
        temp = []
        for i in split:
            new = i
            if i and namespace:
                new = ':'.join([namespace, i])
            
            temp.append(new)
        
        return splitter.join(temp)
    
    def getSceneNamespaces(self):
        result = []
        temp = self._cmds.namespaceInfo(lon=1)
        for i in temp:
            if i not in ("UI", "shared"):
                result.append(i)
        #print 'namespaces:',temp
        return result
    
    def clearSceneNamespaces(self):
        for i in self.getSceneNamespaces():
            self.removeObjectNamespaces(i)
    
    def getIsolatedVetices(self):
        allObject = []
        allDecimalList = []
        newObjectDic = {}
        objectDic = {}
        
        all = self._cmds.ls(type="mesh")
        
        for i in all:
            root = self._pm.PyNode(i)
            A = root.listRelatives(ap=True)
            objectName = A[0].longName()#.split("|")[-1]
            allObject.append(objectName)
        
        allObject=list(set(allObject))
        for  i in allObject: 
            vertexNum = self._cmds.polyEvaluate(i,v=True)
            #print i,vertexNum
            if type(vertexNum) == int:
                decimalList= []
                for ver in range(0,vertexNum):
                    vertexName = i+".vtx["+str(ver)+"]"
                    pointPosition = self._cmds.pointPosition(vertexName)
                    
                    decimalList.append(pointPosition)
                objectDic[i] = decimalList
                
                allDecimalList.append(decimalList)
        
        for key in objectDic:
            verList = objectDic[key]
            dic = {}
            
            for i in verList:
                if verList.count(i)>1:
                    dic[str(i)] = verList.count(i)
            
            if dic:
                newObjectDic[key] = dic
        
        return newObjectDic
    
    def getIsolatedFaces(self):
        errorPoly = []
        all = self._cmds.ls(type="mesh")
        for i in all:
            att = self._cmds.polyEvaluate(i)
            #print i, att
            if att["face"] == 1:
                errorPoly.append(i)
        #print errorPoly        
        
        return errorPoly
    
    def getNPolygonFaces(self, n=4):
        filterSides = n
        
        allMultilateralFace = {}
        all = self._cmds.ls(type="mesh")
        
        for i in all:
            root = self._pm.PyNode(i)
            A = root.listRelatives(ap=True)
            objectName = A[0].longName()#.split("|")[-1]
            faceNum = self._cmds.polyEvaluate(objectName,f=True)
            if type(faceNum) == int:
                multilateralFace = []
                for face in range(0,faceNum):
                    faceName = objectName+".f["+str(face)+"]"
                    edges = self._cmds.polyListComponentConversion(faceName,te=True)
                    vfList = self._cmds.ls( edges, flatten=True )
                    edgesNum = len(vfList)
                    if edgesNum > filterSides:
                        multilateralFace.append(faceName)
                if multilateralFace:        
                    allMultilateralFace[objectName]=multilateralFace
        
        #print allMultilateralFace
        
        return allMultilateralFace
    
    def getOverlappedUVs(self):
        return []
    
    def getUnFreezedObjects(self):
        self._cmds.select(all=True)
        object_name_list = self._cmds.ls(selection=True, transforms=True, geometry=True)
        absent_name = []
        for model_name in object_name_list:
            a = self._cmds.xform(model_name, q=1, ws=1, t=1)
            for xyz in a:
                if int(xyz) != 0:
                    if model_name in absent_name:
                        pass
                    else:
                        absent_name.append(model_name)
                        continue
                else:
                    pass
        self._cmds.select(cl=1)
        return absent_name
    
    def freezeObjects(self, objects):
        if objects:
            objects = ' '.join(objects)
            
            cmd = 'makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 %s;' % objects
            self._mel.eval(cmd)
    
    def getProblemNormals(self):
        cmd = 'polyCleanupArgList 3 { "1","2","1","0","0","0","0","0","0","1.666667","0","0","0","0.181159","0","1","0" };'
        source = self._mel.eval(cmd)
        model_vtx = []
        model_vtx_name_data = {}
        model_name_list = []
        for q in source:
            name = q.split(".")
            if len(model_name_list) == 0:
                model_name_list.append(name[0])
                model_vtx.append(q)
            
            else:
                if name[0] in model_name_list:
                
                    model_vtx.append(q)
                    model_vtx_name_data[name[0]] = model_vtx
                else:
                    
                    model_vtx = []
                    model_name_list.append(name[0])
                    model_vtx.append(q)
        self._cmds.select(cl=1)
        self._cmds.hilite(replace=True)
        
        return model_name_list
    
    def repairNormals(self, obj):
        model_name_list = obj
        if type(model_name_list) == list:
            for model_name in model_name_list:
                self._cmds.select(cl=1)
                self._cmds.select(model_name, r=1)
                self._cmds.polyNormal(normalMode=2)
            self._cmds.select(cl=1)
        
        elif type(model_name_list) == str:
            self._cmds.select(cl=1)
            self._cmds.select(model_name_list, r=1)
            self._cmds.polyNormal(normalMode=2)
            self._cmds.select(cl=1)
    
    def getNonManifoldObjects(self):
        model_name_list = []
        source = self._mel.eval(
            'polyCleanupArgList 3 { "1","2","1","0","0","0","0","0","0","1.666667","0","0","0","0.181159","0","2","0" };')
        for a in source:
            name = a.split(".")[0]
            if name not in model_name_list:
                model_name_list.append(name)
        return model_name_list
    
    def getSmallEdges(self):
        model_name_list = []
        source = self._mel.eval(
            'polyCleanupArgList 3 { "1","2","1","0","0","0","0","0","0","1.666667","1","0.0001","0","0.181159","0","-1","0" };')
        for a in source:
            name = a.split(".")[0]
            if name in model_name_list:
                pass
            else:
                model_name_list.append(name)
        self._cmds.select(cl=1)
        self._cmds.hilite(replace=True)
        return model_name_list
    
    
    #---------------------------------- Materials -------------------------------
    
    def getMaterials(self, removeNamespace=False):
        '''
        Gets materials to a dictionary of which keys are materials and values are
        shapes and faces.
        Example of the returned dictionary:
            {
                'metal': {
                    'box': ['box.face[1-29]', 'box.face[33]'],
                    'sphere': [],
                }
            }
        '''
        shapList = []
        materDic = {}
        
        all = self._cmds.ls(materials=True)
        
        try:
            all.remove("lambert1")
        except:
            pass
        
        try:
            all.remove("particleCloud1")
        except:
            pass
        
        for i in all:
            shad = self._cmds.listConnections(i,type="shadingEngine")
            if shad != None:
                meshlist = self._cmds.sets(shad[0],int=shad[0])
                if meshlist != []:
                    materDic[shad[0]]=meshlist
        #print materDic
        
        for key in materDic.keys():
            for i in materDic[key]:
                if ".f[" in i:
                    shape = self._cmds.listHistory(i,q=1,historyAttr=True)[0].replace(".inMesh","")
                    shapList.append(shape)
                else:
                    shapList.append(i)
        shapList = list(set(shapList))
        #print shapList
        for key in materDic.keys():
            shapeDic ={}
            for st in shapList:
                
                A = []
                for i in materDic[key]:
                    if ".f[" in i:
                        shape = self._cmds.listHistory(i,q=1,historyAttr=True)[0].replace(".inMesh","")
                        
                        root = self._pm.PyNode(shape)
                        mesh  = root.listRelatives(ap=True)
                        newH = mesh[0].longName()
                        if "|" in shape:
                            newSha = newH+"|"+shape.split("|")[-1]
                        else:
                            newSha = newH+"|"+shape
                        #print newSha
                        if shape == st:
                            A.append("|"+i)
                            
                            shapeDic[newSha]=A
                    else:
                        
                        root = self._pm.PyNode(i)
                        mesh  = root.listRelatives(ap=True)
                        newH = mesh[0].longName()
                        
                        if "|" in i:
                            newSha = newH+"|"+i.split("|")[-1]
                        else:
                            newSha = newH+"|"+i
                        shapeDic[newSha]=[]
            #print shapeDic        
            materDic[key] = shapeDic      
        
        #print materDic
        
        result = {}
        if removeNamespace:
            for mat in materDic.keys():
                result[mat] = {}
                
                for shape in materDic[mat].keys():
                    newShape = self.removeStringNamespace(shape)
                    result[mat][newShape] = []
                    
                    for i in range(len(materDic[mat][shape])):
                        value = materDic[mat][shape][i]
                        newValue = self.removeStringNamespace(value)
                        result[mat][newShape].append(newValue)
        
        return result
    
    def exportMaterials(self, path, generateMapping=False, mappingFilename='mapping',
                        removeNamespace=False):
        '''Exports all materials to a new ma file.'''
        materials = self.getMaterials(removeNamespace=removeNamespace)
        
        # Export materials to a file
        #print materials.keys()
        self.select(materials.keys(), replace=True, noExpand=True)
        self.exportSelected(path)
        
        # Generate a json file with materials and geometry relation
        if generateMapping:
            txt = json.dumps(materials, indent=4)
            root = os.path.dirname(path)
            jsonPath = '%s/%s.json' % (root, mappingFilename)
            f = open(jsonPath, 'w')
            f.write(txt)
            f.close()
        
        return materials.keys()
    
    def importMaterials(self, path):
        self.import_(path)
    
    def assignMaterials(self, mapping, geoNamespace='', matNamespace=''):
        '''
        Example of mapping:
            {
                "blinn1SG": {
                    "|dog|base|box|boxShape": [
                        "|box.f[0:5]", 
                        "|box.f[7:9]"
                    ]
                },
                "blinn2SG": {
                    "|dog|base|pCone1|pConeShape1": []
                }
            }
            
            {
                "blinn1SG": {
                    "|dog|base|body|bodyShape": [
                        "|body.f[200:359]", 
                        "|body.f[380:399]"
                    ]
                }, 
                "blinn2SG": {
                    "|dog|base|body|bodyShape": [
                        "|body.f[0:199]", 
                        "|body.f[360:379]"
                    ]
                }
            }
        '''
        for mat in mapping.keys():
            for shape in mapping[mat].keys():
                # The material is assigned to object faces
                if mapping[mat][shape]:
                    # shape: |dog|base|body|bodyShape
                    faces = []
                    for i in mapping[mat][shape]:
                        # i: |body.f[200:359]
                        f = i.split('.')[-1]
                        # f: f[200:359]
                        newI = '%s.%s' % (shape, f)
                        
                        new = self.addObjectNamespace(newI, geoNamespace)
                        # new: |dog:dog|dog:base|dog:body|dog:bodyShape.f[200:359]
                        
                        faces.append(new)
                    
                    faces = ' '.join(faces)
                
                # The material is assigned to the object
                else:
                    faces = ''
                
                # Source is the material
                src = self.addObjectNamespace(mat, matNamespace)
                
                # Destination is the geometry
                dst = "%s.instObjGroups[0]" % shape
                dst = self.addObjectNamespace(dst, geoNamespace)
                
                kwargs = {
                    'source': src,
                    'destination': dst,
                    'connectToExisting': True,
                }
                if faces:
                    kwargs['navigatorDecisionString'] = faces
                
                try:
                    #print kwargs
                    self._cmds.defaultNavigation(**kwargs)
                except:
                    pass
    
    def getFileNodes(self, materials):
        '''
        Gets file texture nodes for the materials.
        materials is a list of material names.
        '''
        fileNodes = []
        for mat in materials:
            nodes = self._cmds.listConnections(mat)
            for node in nodes:
                temp = self._cmds.listConnections(node, type="file")
                if temp:
                    if temp[0] not in fileNodes:
                        fileNodes.append(temp[0])
        
        return fileNodes
    
    def getTexturePaths(self, fileNodes):
        '''Gets texture paths for the file nodes.'''
        texDic = {}
        texError = []
        
        for fn in fileNodes:
            texPath = self._cmds.getAttr("%s.fileTextureName"%fn)
            if os.path.exists(texPath):
                texDic[fn] = texPath
            else:
                texError.append(u'%s节点的贴图路径不存在%s'%(fn,texPath))
        
        return texDic
    
    def replaceTexturePaths(self, maPath, pathInfo):
        #print exportPath,"########################"
        f = open(maPath, "r")
        txt = f.read()
        f.close()
        
        for key in pathInfo.keys():
            txt = txt.replace(key, pathInfo[key])
        
        f = open(maPath, "w")
        f.write(txt)
        f.close()
    
    
    #---------------------------------- Render -------------------------------
    
    def getActiveCamera(self):
        panel_views = self._cmds.getPanel(visiblePanels=True)
        if panel_views:
            return self._cmds.modelPanel(panel_views[0], q=True, cam=True)
    
    def setActiveCameraAttributes(self, filmPivot=False, filmOrigin=False,
                                  safeAction=False, resolution=False, gateMask=False):
        '''Sets display attributes of the active camera.'''
        kwargs = vars().copy()
        del kwargs['self']
        
        camera = self.getActiveCamera()
        if camera:
            for arg in kwargs.keys():
                attr = '%s.display%s%s' % (camera, arg[0].upper(), arg[1:])
                self._cmds.setAttr(attr, kwargs[arg])
    
    def removeAllHUDs(self):
        allHUD = self._cmds.headsUpDisplay(listHeadsUpDisplays=True, q=True)
        if allHUD:
            for hud in allHUD:
                self._cmds.headsUpDisplay(hud, remove=True)
        self._cmds.headsUpDisplay('HUDIKSolverState', section=0, block=5)
    
    def setHUD(self, name='', section=1, block=1, blockSize='small', labelWidth=70,
               label='', labelFontSize='large'):
        '''Sets the heads up display.'''
	#print 'HUD:',vars()
	
        kwargs = vars().copy()
        del kwargs['self']
        
        name = kwargs['name']
        del kwargs['name']
        
        if name:
            self._cmds.headsUpDisplay(name, **kwargs)
        else:
            self._cmds.headsUpDisplay(**kwargs)
    
    def setHUDs(self, data):
        '''
        Sets a list of HUD items.
        data is a list of dictionaries like this:
        [
            {'name': 'combo', 'section': 1, 'block': 1, 'blockSize': 'small',
            'labelWidth': 70, 'label': 'TST', 'labelFontSize': 'large'},
            {},
        ]
        '''
        for d in data:
            #print 'HUD:', d
            self.setHUD(**d)
    
    def playblast(self, path, scale=50, quality=100, resolution=None, override=False):
        '''
        Makes playblast for the current scene.
        Arguments:
            path: a image sequence or a avi file
                image sequence:
                    /abc/abc.####.jpg
                avi:
                    /abc/abc.avi
            scale: percent of the output image
            quality: quality of the output image
            resolution: a list of width and height, default is from render setting dialog
        '''
        f = fllb.parseSequence(path)
        '''
        f:
            {'basename': 'abc',
             'directory': 'C:/jinxi',
             'extension': 'jpg',
             'padding': '%06d',
             'padding_length': 6
             }
        '''
        
        if not resolution:
            resolution = self.resolution()
        
        kwargs = {
            'sequenceTime': 0,
            'clearCache': 1,
            'viewer': 0,
            'showOrnaments': 1,
            'forceOverwrite': override,
            'percent': scale,
            'quality': quality,
            'widthHeight': resolution,
            'framePadding': f['padding_length']
        }
        
        ext = f['extension']
        if ext == 'avi':
            kwargs['format'] = ext
            kwargs['filename'] = path
        
        else:
            kwargs['format'] = 'image'
            kwargs['compression'] = ext
            kwargs['filename'] = '{directory}/{basename}'.format(**f)
        
        self._cmds.playblast(**kwargs)
        
        return True
    
    def makeSceneThumbnail(self, path):
        '''Makes a snapshot image as the scene thumbnail.'''
        x = []
        y = []
        z = []
        _x = []
        _y = []
        _z = []
        allObject = []
        
        allT = self._cmds.ls(type="mesh")
        for i in allT:
            root = self._pm.PyNode(i)
            A = root.listRelatives(ap=True)
            objectName = A[0].longName()
            allObject.append(objectName)
        
        for i in allObject:
            si = self._cmds.xform(i,q=1,bb=1)
            #print i,si
            x.append(si[0])
            y.append(si[1])
            z.append(si[2])
            _x.append(si[3])
            _y.append(si[4])
            _z.append(si[5])
        size = [min(x),min(y),min(z),max(_x),max(_y),max(_z)]
        
        x = (size[0]+size[3])/2
        y = (size[1]+size[4])/2
        z = (size[2]+size[5])/2
        
        maxLength = [abs(size[0])+abs(size[3]),
                     abs(size[1])+abs(size[4]),
                     abs(size[2])+abs(size[5])]
        
        # Get current view
        camera_views = None
        panel_views = self._cmds.getPanel(visiblePanels=True)
        for view in panel_views:
            try:
                camera_views = self._cmds.modelPanel(view, q=True, cam=True)
            except:
                pass
            #RuntimeError: modelPanel: Object 'scriptEditorPanel1' not found.
        
        cameraname = self._cmds.camera()
        
        self._cmds.move(x,y+max(maxLength)*0.7,z+max(maxLength)*1.2,cameraname[0])
        #self._cmds.rotate( '-30deg',0 , 0,cameraname[0])#'-45deg'
        
        self._cmds.rotate( '-30deg',0 , 0,cameraname[0])#'-45deg'
        self._cmds.move(x,y,z,"%s.scalePivot"%cameraname[0],"%s.rotatePivot"%cameraname[0])
        self._cmds.setAttr("%s.rotateY"%cameraname[0] ,45)
        self._cmds.lookThru(cameraname[0])
        
        currentTime = self.currentFrame()
        baseName,ext = os.path.splitext(path)
        ext = ext.replace('.','')
        
        self._cmds.playblast(filename=baseName, startTime=currentTime, endTime=currentTime,
                             sequenceTime=0, clearCache=1,viewer=0,showOrnaments=0,
                             fp=0, percent=50, format="image", compression=ext,
                             quality=70, widthHeight=[512,512])
        
        self._cmds.delete(cameraname)
        
        if camera_views:
            self._cmds.lookThru(camera_views)
        
        result = '%s.%d.%s' % (baseName, currentTime, ext)
        if os.path.exists(path):
            os.remove(path)
        os.rename(result, path)
    
    
    #---------------------------------- Dialog -------------------------------
    
    def confirmDialog(self, *args, **kwargs):
        return self._cmds.confirmDialog(*args, **kwargs)
    
    def newSceneConfirmDialog(self):
        btn1 = 'Save'
        btn2 = "Don't Save"
        btn3 = 'Cancel'
        kwargs = {
            'title': 'Warning: Scene Not Saved',
            'message': 'Save changes?', 
            'button': [btn1, btn2, btn3], 
            'defaultButton': btn1,
            'cancelButton': btn3,
            'dismissString': btn2,
        }
        confirm = self._cmds.confirmDialog(**kwargs)
        #print confirm
        
        if confirm == btn1:
            return True
        elif confirm == btn2:
            return False
    
    def saveAsFileDialog(self):
        multipleFilters = "Maya ASCII (*.ma);;Maya Binary (*.mb)"
        filename = self._cmds.fileDialog2(fileMode=0, caption="Save As",
                                          fileFilter=multipleFilters)
        
        if filename:
            return filename[0]

    def newDialog(self):
        if self.hasUnsavedChanges():
            confirm = self.newSceneConfirmDialog()
            if confirm == True:
                result = self.saveDialog()
                if result:
                    self.new(force=True)
                    return True
                else:
                    return False
            
            elif confirm == False:
                self.new(force=True)
                return True
        
        else:
            self.new(force=True)
            return True
    
    def saveDialog(self):
        if self.isUntitled():
            path = self.saveAsFileDialog()
            if path:
                self.saveAs(path, force=True)
                return True
            
            else:
                return False
        
        else:
            self.save(force=True)
            return True

