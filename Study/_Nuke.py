#!/usr/bin/env python
# -*- coding:utf-8 -*-
#在用户界面创建类似 menu toolbar的响应节点，使用下面语法:
nuke.createNode( "nodename" )
#创建节点时添加必要的控制属性，语法如下：
nuke.nodes.node( control = value )
#添加一个节点，并赋值给变量：
variable = nuke.nodes.nodename()
b = nuke.nodes.Blur()
b["size"].setValue( 10)
#通过名字去读节点：
nuke.toNode( " dagnodename" )
#读取节点中选取的节点
#获取当前选择的节点：
selectNode = nuke.selectedNode()
#如果选了多个节点，nuke返回最底部的节点。
#想读取所有的节点，请使用：
selectNodes = nuke.selectNodes() #返回选择的列表
#给节点添加控制
b = nuke.nodes.Blur()
k = nuke.Array_Knob("myctrl", "My Control" )
b.addKnob(k)
#隐藏和展示节点的属性panel
#使用showControlPanel() hideControlPanel() 函数来设置一个节点的属性面板的打开与关闭。例如，展示新节点Blur的属性面板：
#创建节点的时候不打开属性面框
nuke.createNode( "Blur", inpanel = True)
#连接节点，并设置输入
r1 = nuke.nodes.Read(file="filepath/filename.ext")
r2 = nuke.nodes.Read(file="filePaht/filename.ext")
m = nuke.nodes.Merge(inputs=[r2, r1])
#给属性设定默认值
# 可以给属于同一个类的节点设置控制的默认值。当默认值设置后，所有名字相同的控制都会是这个值。
#例如，想设置所有Blur节点的size
#控制为20：
nuke.knobDefault("Blur.size", "20")
#把项目设置中frame范围的最后frame设置为200：
nuke.knobDefault("Root.last_frame", "200")
#渲染时使用Write节点
#用脚本添加了Write节点，现在要渲染1-35帧。
#渲染一个单独的节点：
nuke.execute(" name", start, end, incr )
#在我们的例子里：
nuke.execute(" Write1", 1, 35, 2) or nuke.execute("Write1, start=1, end=35, incr=2)
#也可以使用 nuke.render( name, start, end, incr ）

#设置帧范围
frange=nuke.FrameRange()
frange.maxFrame()
#存储多个帧范围
frange=nuke.FrameRanges()
#文件名中标注frame号码
filename = nukescripts.replaceHashes( node['file'].value() )%nuke.frame()

#读取节点元数据
# 获取节点的元数据，并存在字典里：nuke.toNode("Read1").metadata()
# 某一帧或者视口的元数据： nuke.toNode("Read1").metadata("key", frame, "view" )
# 已经在一个节点里加载了双目数据，想找出左眼93帧的修改时间：
nuke.toNode("Read1").metadata("input/mtime", 93, "left")
# 相似，获取右眼95帧文件大小
nuke.toNode("Read1").metadata("input/filesize", 95, "right")
# 获取指定元数据：
nuke.toNode("Read1").metadata("key")
# 例如： nuke.toNode("Read1").metadata("input/ctime")
