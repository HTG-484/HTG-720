#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Author_:@WangTianXiang
import os
import sys
import re
import json
class Maya(object):
    def __init__(self):
        import maya.cmds as cmds
        import pymel.core as pm
        import maya.mel as mel
        import maya.api.OpenMaya as om

        self._cmds =cmds
        self._mel = mel
        self._pm = pm
        self._om = om
    def app(self):
        return 'maya'

# 检查是否勾选相应的相对应函数
    def osbGetRunOnAllObjects(self):
        return menuItem("-q", "-checkBox", "osbRunOnAllGeoCB")
#查找开口边
    def osbSanityBorders(self):
        if (self.osbGetRunOnAllObjects()):
            self._cmds.select(self._cmds.ls(exactType='mesh'))
        self._cmds.polySelectConstraint(mode=3, t=0x8000, w=1)
        self._cmds.polySelectConstraint(dis=True)
#修复开口边，将其补洞
    def osbSanityBordersFix(self):
        for i in self._cmds.ls(sl=1):
            self._cmds.polyCloseBorder(i, ch=1)
        self._cmds.select(cl=True)
#查找点重合的物体
    def osbSanityZeroLengthEdges(self):
        if self.osbGetRunOnAllObjects():
            self._mel.eval('polyCleanupArgList 3 {"1","2","1","0","0","0","0","0","0","1e-005","1","0","0","1e-005","0","-1","0" };')
#修复点重合的物体
    def osbSanityZeroLengthEdgesFix(self):
        if self.osbGetRunOnAllObjects():
            self._mel.eval('polyCleanupArgList 3 {"1","1","1","0","0","0","0","0","0","1e-005","1","1e-05","0","1e-005","0","-1","0" };')
#查找存在多边面
    def osbSanityMoreThanFourEdges(self):
        if self.osbGetRunOnAllObjects():
            self._mel.eval('polyCleanupArgList 3 {"1","2","1","0","1","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-2","0" };')
#修复多边面
    def osbSanityMoreThanFourEdgesFix(self):
        if self.osbGetRunOnAllObjects():
            self._mel.eval('polyCleanupArgList 3 {"1","1","1","0","1","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1","0" };')
#查找非法面
    def osbSanityNonManifoldFaces(self):
        if self.osbGetRunOnAllObjects():
            self._mel.eval('polyCleanupArgList 3 {"1","2","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","2","0" };')
#修复非法面
    def osbSanityNonManifoldFacesFix(self):
        if self.osbGetRunOnAllObjects():
            self._mel.eval('polyCleanupArgList 3 {"1","1","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","2","0" };')
#查找悬空面

    def osbSanityLaminaFaces(self):
        if self.osbGetRunOnAllObjects():
            self._mel.eval('polyCleanupArgList 3 {"1","2","1","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-1","1" };')
#修复悬空面
    def osbSanityLaminaFacesFix(self):
        if self.osbGetRunOnAllObjects():
            self._mel.eval('polyCleanupArgList 3 {"1","1","1","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-2","1" };')

#查找带点位移的几何体
    def getMesh(self,obj):
        '''
        判断是否为mesh
        :param obj:
        :return: string
        '''
        type = self._cmds.objectType(obj)
        if type == 'mesh':
            return obj
        elif type == 'transform':
            shape = self._cmds.listRelatives(obj, type='mesh')
            return shape[0]
        self._cmds.error("Don't get here")

    def getMeshesFromSelection(self):
        '''
        从选择中获得mesh
        :return:list
        '''
        sl = self._cmds.ls(sl=True)
        meshes = []
        for s in sl:
            meshes.append(self.getMesh(s))
        return meshes

    def getObjectsBasedOnPrefs(self):
        '''
        是从选择中获取，还是默认获取场景中的物体
        :return:
        '''
        if self.osbGetRunOnAllObjects():
            sl = self._cmds.ls(exactType='mesh')
        else:
            sl = self.getMeshesFromSelection()
        return sl

    def getShape(self,shape):
        '''
        返回mesh的shape
        :param shape:
        :return:string
        '''
        parents = self._cmds.listRelatives(shape, p=True, f=True)
        shapes = self._cmds.listRelatives(parents[0], s=True, f=True, ni=True, type='shape')
        if shapes[0] == shape:
            return shape
        else:
            return ""

    def blpMeshVtxPos(self):
        '''
        运行此函数查找存在点位移的几何体
        :return:
        '''
        sl = self.getObjectsBasedOnPrefs()
        self._cmds.select(cl=True)
        for s in sl:
            sfList = self._cmds.ls(s, type='mesh', l=True)
            sf = sfList[0]
            trueShape = self.getShape(sf)
            if (len(trueShape) > 0):
                verts = self._cmds.polyEvaluate(sf, v=True)
                for i in range(verts + 1):
                    check = []
                    j = float(self._cmds.rand(verts))
                    pnx = float(self._cmds.getAttr(sf + ".pnts[" + str(j) + "].pntx"))
                    pny = float(self._cmds.getAttr(sf + ".pnts[" + str(j) + "].pnty"))
                    pnz = float(self._cmds.getAttr(sf + ".pnts[" + str(j) + "].pntz"))
                    pre = 0.00001
                    if (((pnx < 0 - pre) | (pnx > 0 + pre)) | ((pny < 0 - pre) | (pny > 0 + pre)) | (
                        (pnz < 0 - pre) | (pnz > 0 + pre))):
                        parent = self._cmds.listRelatives(sf, allParents=True, f=True)
                        check.append(parent[0])
                        self._cmds.select(parent[0], add=True)
                    if (len(check) > 0):
                        del check[:]
                        break

    def blpMeshVtxPosFix(self):
        '''
        修复存在点位移的几何体
        :return:
        '''
        ls = self._cmds.ls(sl=True)
        for s in ls:
            step1 = self._cmds.polyNormal(s, normalMode=0)
            step2 = self._cmds.polyNormal(s, normalMode=0)
            self._cmds.delete(step1[0], step2[0])

    def getParents(self,obj):
        '''
        得到物体的父节点
        :param obj:
        :return:
        '''
        relatives = self._cmds.listRelatives(obj, parent=1, f=1)
        #	return relatives
        if relatives == None:
            return 0

    def blpTransformChangeFix(self):
        '''
        冻结位置坐标
        :return:
        '''
        list = self._cmds.ls(sl=1)
        for s in list:
            self._cmds.makeIdentity(s, apply=True, t=1, r=1, s=1, n=0)

    def blpLocalPivotChangeFix(self):
        '''
        设置中心坐标点
        :return:
        '''
        ls = self._cmds.ls(sl=True)
        for s in ls:
            self._cmds.xform(s, cp=True)



    def blpObjPivotToZeroFix(self):
        '''
        设置重心坐标点到轴心
        :return:
        '''
        list = self._cmds.ls(sl=1)
        for s in list:
            self._cmds.move(0, 0, 0, s + ".scalePivot", s + ".rotatePivot")

#检查一个物体是否有多个shape节点

    def blpMoreShape(self):
        if self.osbGetRunOnAllObjects():
            sl = self._cmds.ls(exactType="transform")
            self._cmds.select(cl=True)
        else:
            sl = self._cmds.ls(sl=True)
            self._cmds.select(cl=True)
        for s in sl:
            shapes = self._cmds.listRelatives(s, s=True, f=True, ni=True)
            if len(shapes) > 1:
                self._cmds.select(s, add=True)
#修复一个物体多个shape节点的问题
    def blpMoreShapeFix(self):
        ls = self._cmds.ls(sl=True)
        for s in ls:
            shapes = self._cmds.listRelatives(s, s=True, f=True, ni=True)
            del shapes[0]
            self._cmds.delete(shapes)

# 如果场景中存在references物件就给与警告
    def osbSanityWarnRefMaterial(self):
        refs = self._cmds.ls(referencedNodes=True)
        if len(refs) > 0:
            self._cmds.confirmDialog(title="Referenced nodes", message="这个场景存在References物体或材质", button="Ok")

# 检查是否存在中间物（导致无法删除历史的节点）

    def osbAddSanityCheck(self,name, category, description, help, type):
        osbSanityChecks = []
        osbSanityDescriptions = []
        osbSanityHelp = []
        osbSanityCategories = []
        osbSanityTypes = []
        osbSanityChecks.append(name)
        osbSanityDescriptions.append(category)
        osbSanityHelp.append(description)
        if help != '':
            osbSanityCategories.append(help)
        elif help == '':
            osbSanityCategories.append(description)
        osbSanityTypes.append(type)


    osbAddSanityCheck("blpDeleteIntermediateObject", "GEO CHECK", "检查是否存在中间物（导致无法删除历史的节点）", "This checks whether the normals for the object are facing 'outwards'.It uses a combination of two statistical methods to do so, and selects the method with the highest level of confidence. Please note that this check assumes that normals are conformed before running.", "Perform,Select,fix")

    def blpDeleteIntermediateObject(self):
        pass
    def blpDeleteIntermediateObject(self):
        '''
        调用osbAddSanityCheck(),getObjectsBasedOnPrefs(),检查是否存在中间物（导致无法删除历史的节点）并删除其shapeName
        :return:
        '''
        self.osbAddSanityCheck("blpDeleteIntermediateObject", "GEO CHECK", "检查是否存在中间物（导致无法删除历史的节点）","This checks whether the normals for the object are facing 'outwards'.It uses a combination of two statistical methods to do so, and selects the method with the highest level of confidence. Please note that this check assumes that normals are conformed before running.","Perform,Select,fix")


        sl = self.getObjectsBasedOnPrefs()
        self._cmds.select(cl=True)
        for s in sl:
            if self._cmds.getAttr(s + ".intermediateObject") == 1:
                self._cmds.select(s, add=True)

    def blpDeleteIntermediateObjectFix(self):
        ls = self._cmds.ls(sl=True)
        for s in ls:
            self._cmds.delete(s)

#'是否存在关联复制物体'

    osbAddSanityCheck("blpInstanceObj", "GEO CHECK", "是否存在关联复制物体", "This check deletes history on all nodes.", "Perform,Select,fix")

    def blpInstanceObj(self):
        pass
    def blpInstanceObj(self):
        '''
        调用osbAddSanityCheck(),getObjectsBasedOnPrefs(),是否存在关联复制物体,是，则选中被关联复制出的物体
        :return:
        '''
        self.osbAddSanityCheck("blpInstanceObj", "GEO CHECK", "是否存在关联复制物体", "This check deletes history on all nodes.","Perform,Select,fix")

        sl = self.getObjectsBasedOnPrefs()
        print sl
        self._cmds.select(cl=True)
        for s in sl:
            print s
            all_parents = self._cmds.listRelatives(s, allParents=True)
            print all_parents
            all_parents_num = len(all_parents)
            if all_parents_num > 1:
                shape_parents = self._cmds.listRelatives(s, p=True)
                for instance_obj in all_parents:
                    if instance_obj != shape_parents[0]:
                        self._cmds.select(instance_obj, add=True)

#'检查Shape节点名称是否匹配变换节点'


    osbAddSanityCheck("blpMatchShapeName", "GEO CHECK", "检查Shape节点名称是否匹配变换节点", "This check matching shape nodes name from transform nodes.", "Perform,Select,fix")

    def blpMatchShapeName(self):
        pass
    def blpMatchShapeName(self):
        '''
        调用osbAddSanityCheck(),getObjectsBasedOnPrefs(),检查Shape节点名称是否匹配变换节点,如果不匹配，则shapeName则更改为transformName+shape组合
        :return:
        '''
        self.osbAddSanityCheck("blpMatchShapeName", "GEO CHECK", "检查Shape节点名称是否匹配变换节点","This check matching shape nodes name from transform nodes.", "Perform,Select,fix")

        sl = self.getObjectsBasedOnPrefs()
        self._cmds.select(cl=True)
        for s in sl:
            path = self._cmds.ls(s, l=True)
            array = path[0].split('|')
            for a in array:
                if a == '':
                    array.remove(a)
                else:
                    pass
            orgName = array[len(array) - 1]
            shapeName = array[len(array) - 2] + 'Shape'
            if orgName != shapeName:
                self._cmds.select(s, add=True)

    def blpMatchShapeNameFix(self):
        sl = self._cmds.ls(sl=True)
        for s in sl:
            parents = self._cmds.listRelatives(s, p=True)
            shapeName = parents[0] + 'Shape'
            self._cmds.rename(s, shapeName)

#'是否存在面赋予材质的物体'


    osbAddSanityCheck("blpMoreShaders", "GEO CHECK", "是否存在面赋予材质的物体", "This check deletes history on all nodes.", "Perform,Select,fix")

    def blpMoreShaders(self):
        pass
    def blpMoreShaders(self):
        '''
        调用osbAddSanityCheck(),getObjectsBasedOnPrefs(),检查是否存在面赋予材质的物体，若存在，则添加选择
        :return:
        '''
        self.osbAddSanityCheck("blpMoreShaders", "GEO CHECK", "是否存在面赋予材质的物体", "This check deletes history on all nodes.","Perform,Select,fix")

        sl = self.getObjectsBasedOnPrefs()
        mat_list = []
        self._cmds.select(cl=True)
        for s in sl:
            shadingEngines = self._cmds.listConnections(s, type="shadingEngine")
            materials = self._cmds.ls(self._cmds.listConnections(shadingEngines), mat=True)
            for m in materials:
                if m not in mat_list:
                    mat_list.append(m)
                else:
                    pass
            mat_num = len(mat_list)
            if mat_num > 1:
                self._cmds.select(s, add=True)

#'删除所有历史'

    osbAddSanityCheck("osbSanityDeleteHistory", "GEO CHECK", "删除所有历史", "This check deletes history on all nodes.", "Perform")

    def osbSanityDeleteHistory(self):pass
    def osbSanityDeleteHistory(self):
        '''
        调用osbAddSanityCheck(),getObjectsBasedOnPrefs(),删除所有存在的物体的历史
        :return:
        '''
        self.osbAddSanityCheck("osbSanityDeleteHistory", "GEO CHECK", "删除所有历史", "This check deletes history on all nodes.","Perform")

        sl = self.getObjectsBasedOnPrefs()
        for s in sl:
            if self._cmds.objExists(s):
                self._cmds.select(s)
                self._mel.eval('DeleteHistory()')
        self._cmds.select(cl=True)


#'检查多边形面的法线方向是否正确（单片物体可忽略检查结果）'

    def checkNormalDirection(self,meshName):
        '''
        通过对传入进来的mesh或者obj进行判断，若面法线反，则返回inwards
        :param meshName:
        :return:
        '''
        if '[' and ']' in meshName:
            selList = self._om.MSelectionList()  # MSelectionList是存储在MAYA中被选中的物体集
            selList.add(meshName)
            mesh = self._om.MFnMesh(selList.getDependNode(0))  # 初始化新的MFnMesh对象并将其附加到网格节点或网格数据对象
            first_split = meshName.split('.')  # Result: ['pPlane1', 'f[90]']
            second_split = first_split[1].split('f')  # Result: ['', '[90]']
            third_split = second_split[1].split('[')  # Result: ['', '90]']
            forth_split = third_split[1].split(']')  # Result: ['90', '']
            final_fid = int(forth_split[0])
            uvA = mesh.getPolygonUV(final_fid, 0)  # 返回指定多边形的UV的U值和V值
            uvB = mesh.getPolygonUV(final_fid, 1)
            uvC = mesh.getPolygonUV(final_fid, 2)
            vAB = self._om.MPoint(uvB[0], uvB[1]) - self._om.MPoint(uvA[0], uvA[1])  # 坐标运算
            vBC = self._om.MPoint(uvC[0], uvC[1]) - self._om.MPoint(uvB[0], uvB[1])
            Noraml = vAB ^ vBC  # 两个矢量进行叉积
            if Noraml.z < 0:
                return 'inwards'

    def osbSanityNormals(self):
        '''
        调用osbAddSanityCheck(),getObjectsBasedOnPrefs(),checkNormalDirection(),对选中的物体或者面，或者什么也不选择，判断是否有面的发现为反，若存在，则选中
        :return:
        '''
        self.osbAddSanityCheck("osbSanityNormals", "GEO CHECK", "检查多边形面的法线方向是否正确（单片物体可忽略检查结果）","This checks whether the normals for the object are facing 'outwards'.It uses a combination of two statistical methods to do so, and selects the method with the highest level of confidence. Please note that this check assumes that normals are conformed before running.","Perform,Select,fix");

        meshes = self.getObjectsBasedOnPrefs()
        self._cmds.select(cl=True)
        for s in meshes:
            print("checkNormalDirection + " + s + "\n")
            if self._cmds.objExists(s) == False:
                self._cmds.error(s + "does not exist\n")
            elif '[' and ']' and ':' in s:
                first_split = s.split('.')  # Result: ['pPlane1', 'f[90:94]']
                second_split = first_split[1].split('f')  # Result: ['', '[90:94]']
                third_split = second_split[1].split('[')  # Result: ['', '90:94]']
                forth_split = third_split[1].split(']')  # Result: ['90:94', '']
                fifth_split = forth_split[0].split(':')  # Result: ['90', '94']
                final_fid = int(fifth_split[1]) - int(fifth_split[0]) + 1
                for f in range(final_fid):
                    next_s = first_split[0] + '.' + 'f[' + str(int(fifth_split[0]) + f) + ']'
                    dir = self.checkNormalDirection(next_s)
                    if dir == 'inwards':
                        self._cmds.select(next_s, add=True)
            elif '[' and ']' in s and ':' not in s:
                dir = self.checkNormalDirection(s)
                if dir == 'inwards':
                    self._cmds.select(s, add=True)

            elif '[' and ']' not in s:
                selList = self._om.MSelectionList()  # MSelectionList是存储在MAYA中被选中的物体集
                selList.add(s)
                mesh = self._om.MFnMesh(selList.getDependNode(0))  # 初始化新的MFnMesh对象并将其附加到网格节点或网格数据对象
                for m in range(mesh.numPolygons):
                    next_s = s + '.' + 'f[' + str(m) + ']'
                    dir = self.checkNormalDirection(next_s)
                    if dir == 'inwards':
                        self._cmds.select(next_s, add=True)

    def osbSanityNormalsFix(self):
        '''
        调用checkNormalDirection(),若有面法线为反，并且被选中，则对其进行反转，使其面法线为正
        :return:
        '''
        shapesInSel = self._cmds.ls(dag=1, o=1, s=1, sl=1)
        for meshName in shapesInSel:
            revFaces = []
            selList = self._om.MSelectionList()  # MSelectionList是存储在MAYA中被选中的物体集
            selList.add(meshName)
            mesh = self._om.MFnMesh(selList.getDependNode(0))  # 初始化新的MFnMesh对象并将其附加到网格节点或网格数据对象
            for fid in range(mesh.numPolygons):
                uvA = mesh.getPolygonUV(fid, 0)  # 返回指定多边形的UV的U值和V值
                uvB = mesh.getPolygonUV(fid, 1)
                uvC = mesh.getPolygonUV(fid, 2)
                vAB = self._om.MPoint(uvB[0], uvB[1]) - self._om.MPoint(uvA[0], uvA[1])  # 坐标运算
                vBC = self._om.MPoint(uvC[0], uvC[1]) - self._om.MPoint(uvB[0], uvB[1])
                Noraml = vAB ^ vBC  # 两个矢量进行叉积
                if Noraml.z < 0:
                    revFaces.append('%s.f[%i]' % (meshName, fid))
            if len(revFaces) > 0:
                self._cmds.polyNormal(normalMode=0, userNormalMode=0, ch=1)  # 对法线进行反转
            else:
                print '未发现法线错误的面'
        self._cmds.select(cl=True)


#'是否有几何体和组的中心轴被改动'

    osbAddSanityCheck("blpLocalPivotChange", "TRANSFORM CHECK", "是否有几何体和组的中心轴被改动","This check deletes history on all nodes.", "Perform,Select,fix")

    def blpLocalPivotChange(self):
        if self.osbGetRunOnAllObjects():
            sl = self._cmds.ls(et="transform")
            self._cmds.select(clear=True)
        else:
            sl = self._cmds.ls(sl=True)
            self._cmds.select(clear=True)
        defItem = ['persp', 'front', 'side', 'top']
        checkList = ret = list(set(defItem) ^ set(sl))
        defMatrix = [0, 0, 0]
        noZeroList = []
        pre = 0.00001
        for s in checkList:
            diff_num = 0
            scale_piv = self._cmds.xform(s, q=True, scalePivot=True)
            rotate_piv = self._cmds.xform(s, q=True, rotatePivot=True)
            for i in range(len(defMatrix)):
                if (scale_piv[i] != defMatrix[i] or rotate_piv[i] != defMatrix[i]):
                    diff_num = diff_num + 1
            if diff_num > 0:
                noZeroList.append(s)
        for t in noZeroList:
            obj_diff_num = 0
            obj_scale_piv = self._cmds.getAttr(t + '.scalePivot')[0]
            obj_rotate_piv = self._cmds.getAttr(t + '.rotatePivot')[0]
            bb_matrix = self._cmds.objectCenter(t, l=True)
            for n in range(len(bb_matrix)):
                if (obj_scale_piv[n] - bb_matrix[n] < 0 - pre or obj_scale_piv[n] - bb_matrix[n] > 0 + pre or
                        obj_rotate_piv[n] - bb_matrix[n] < 0 - pre or obj_rotate_piv[n] - bb_matrix[n] > 0 + pre):
                    obj_diff_num = obj_diff_num + 1
            if obj_diff_num > 0:
                self._cmds.select(t, add=True)


#'是否有几何体和组的中心轴不在世界坐标0点位置'

    osbAddSanityCheck("blpObjPivotToZero","TRANSFORM CHECK","是否有几何体和组的中心轴不在世界坐标0点位置","This check deletes history on all nodes.","Perform,Select,fix")

    def blpObjPivotToZero(self):
        sl = []
        if self.osbGetRunOnAllObjects():
            sl = self._cmds.ls(exactType="transform")
            self._cmds.select(cl=1)
        else:
            sl = self._cmds.ls(sl=1)
            self._cmds.select(cl=1)

        defItems = ["persp", "front", "side", "top"]
        checkList = [i for i in sl if i not in defItems]  # 求列表ls与列表defItems的差集
        defMatrix = [0, 0, 0]
        for s in checkList:

            diff_num = 0
            scale_piv = self._cmds.xform(s, q=1, scale=1)
            rotate_piv = self._cmds.xform(s, q=1, rotation=1)

            for i in range(len(defMatrix)):
                if (scale_piv[i] != defMatrix[i] and rotate_piv[i] != defMatrix[i]):
                    diff_num = diff_num + 1
            if (diff_num > 0):
                self._cmds.select(s, add=1)

#'检查物体顶层是否符合只有1个组的规范并把该组轴心归零'

    osbAddSanityCheck("osbSanityTopGroupNodeToZero","TRANSFORM CHECK","检查物体顶层是否符合只有1个组的规范并把该组轴心归零","This places the top level group node's pivot at world (0,0,0)\n\This check will not work if there is more than 1 top group transform.","Perform")

    def osbSanityTopGroupNodeToZero(self):

        # get all transforms that don't have any parents

        trans = self._cmds.ls(exactType="transform")
        topLevel = []
        for s in trans:
            if (self.getParents(s) == 0 and s != "top" and s != "side" and s != "front" and s != "persp"):
                topLevel.append(s)
        print topLevel
        # there can be only one
        if (len(topLevel) > 1):
            self._cmds.confirmDialog(title='Top Level Nodes', message=u'警告根据规范每个资产元素顶层应该只有一个组', button="OK")
        if (len(topLevel) == 1):
            self._cmds.move(0, 0, 0, topLevel[0] + ".scalePivot", topLevel[0] + ".rotatePivot")

#'为物体创建测量工具显示测量结果（生成的内容可用清理场景指令清除）'

    osbAddSanityCheck("blpMeasureTool","TRANSFORM CHECK","为物体创建测量工具显示测量结果（生成的内容可用清理场景指令清除）","This places the top level group node's pivot at world (0,0,0)\n\This check will not work if there is more than 1 top group transform.","Perform")

    def blpMeasureTool(self):
        trans = self._cmds.ls(et="transform")
        topLevel = []
        a = 1
        for s in trans:
            if (s == 'measureTool_blp'):
                self._cmds.delete('measureTool_blp')
            elif (self.getParents(s) == 0 and s != 'top' and s != 'side' and s != 'front' and s != 'persp'):
                topLevel.append(s)
        if len(topLevel) > 1:
            self._cmds.confirmDialog(title='Top Level Nodes', message=u'警告根据规范每个资产元素顶层应该只有一个组', button='OK')
        if len(topLevel) == 1:
            topObj = topLevel[0]
            pivs = self._cmds.xform(topObj, q=True, ws=True, piv=True)
            piv = []
            piv_0 = (pivs[0] + pivs[3]) / 2.0
            piv.append(piv_0)
            piv_1 = (pivs[1] + pivs[4]) / 2.0
            piv.append(piv_1)
            piv_2 = (pivs[2] + pivs[5]) / 2.0
            piv.append(piv_2)
            cube = self._cmds.polyCube()  # 多维数据集命令创建一个新的多边形立方体。
            self._cmds.connectAttr((topObj + '.boundingBox.boundingBoxSize'), (cube[0] + '.scale'))  # 连接两个依赖节点的属性并返回两个连接属性的名称
            self._cmds.move(piv[0], piv[1], piv[2], cube[0], ws=True)
            scaleY = self._cmds.getAttr(cube[0] + '.scaleY')
            measures = self._cmds.distanceDimension(sp=(0, 0, 0), ep=(0, scaleY, 0))  # 这个命令是用来创建一个距离维度来显示两个指定点之间的距离。
            locs = self._cmds.listConnections(measures)  # 这个命令返回一个列表的所有属性/指定类型的对象连接到给定对象
            goupName = self._cmds.group(measures, locs, n='measureTool_blp')  # 这个命令组指定的对象在一个新的组,并返回新组的名称
            self._cmds.delete(cube)

# '是否有几何体与地面穿插'

    osbAddSanityCheck("osbSanityGeoAtZero","TRANSFORM CHECK","是否有几何体与地面穿插","This check ensures that no geometry's bounding box is below -0.005","Perform,Select,fix")

    def osbSanityGeoAtZero(self):
        obj = []
        sl = self.getObjectsBasedOnPrefs()
        for s in sl:
            bb = self._cmds.polyEvaluate(s, b=1)
            if bb[1][0] < -0.005:
                obj.append(s)
        self._cmds.select(obj)

#'冻结变形属性'

    osbAddSanityCheck("osbSanityFreezTransforms","TRANSFORM CHECK","冻结变形属性","Freezes all transform nodes in the scene","Perform")

    def osbSanityFreezTransforms(self):
        if self.osbGetRunOnAllObjects():
            selectlist = self._cmds.ls(exactType="transform")
            self._cmds.select(cl=True)
        else:
            selectlist = self._cmds.ls(sl=1)
            self._cmds.select(cl=True)

        for s in selectlist:
            self._cmds.makeIdentity(s, apply=True, t=1, r=1, s=1, n=0)

#'是否有几何体和组未冻结'

    osbAddSanityCheck("blpTransformChange","TRANSFORM CHECK","是否有几何体和组未冻结","This check deletes history on all nodes.","Perform,Select,fix")

    def blpTransformChange(self):
        sl = []
        checkList = []

        if self.osbGetRunOnAllObjects():
            sl = self._cmds.ls(exactType="transform")
            self._cmds.select(cl=1)
        else:
            sl = self._cmds.ls(sl=1)
            self._cmds.select(cl=1)

        defItems = ["persp", "front", "side", "top"]
        checkList = [i for i in sl if i not in defItems]  # 求列表ls与列表defItems的差集
        defMatrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

        for s in checkList:
            diff_num = 0
            matrix = self._cmds.getAttr(s + ".matrix")  # 返回所有的位置坐标

            for i in range(len(defMatrix)):

                if (matrix[i] != defMatrix[i]):
                    diff_num = diff_num + 1

            if (diff_num > 0):
                self._cmds.select(s, add=1)



