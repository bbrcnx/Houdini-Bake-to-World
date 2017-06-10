#v1.0 2017_06_10 Author:wang xiaowei  Email:wangxiaowei@ckyhvfx.com
#This script will bake local space animation of objects into worldspace animation.


range = hou.playbar.playbackRange()
start = range[0]
end = range[1]


sel_nodes=hou.selectedNodes()

#check if there is a node selected, if none, raise warning to let user select nodes first.
if sel_nodes == ():
    raise NameError('请先选择节点！')


#Remove the nodes don't have translate and rotation parameters. 
#Put the nodes with the translate and rotation parameters in a new list.
convert_nodes =[]
for node in sel_nodes:
    path = node.path()
    t = hou.parmTuple(path+"/t")
    r = hou.parmTuple(path+"/r")

    if t != None and r != None:
        convert_nodes.append(node)

#If no node have translate or rotation parameter will raise a warning to notice user.
if convert_nodes == []:
    raise NameError("所选择的节点都没有\"translate\"或\"rotation\"参数，无法转换。")


chopnet = hou.node("/obj").createNode("chopnet")
chopnet.moveToGoodPosition()


for old_node in convert_nodes:
    node_path = old_node.path()
    
    #copy convert node to /obj 
    new_node = hou.copyNodesTo([old_node],hou.node("/obj"))[0]
    
    #Rename the copied node to name of the old_node and postfix "_bakeW_1" behind. 
    #And auto increment digit if have same node name.
    new_node.setName(old_node.name() + "_bakeW_1",unique_name = True)

    #If the node have input connection, disconnect it. Otherwise it may not in worldspace.
    if new_node.inputConnections() != ():
        new_node.setInput(0, None)          
    new_node.moveToGoodPosition()
    
    new_node.parmTuple('t').deleteAllKeyframes()    #delete all the translate keyframes
    new_node.parmTuple('r').deleteAllKeyframes()    #delete all the rotation keyframes
    new_node.movePreTransformIntoParmTransform()    #Extract pretransform in case it will cause mis lineup.

    #Create a chopnode "object" and name with the corresponding /obj object node.
    chopobject = chopnet.createNode("object",node_name=old_node.name() + "_")
    chopobject.moveToGoodPosition()
    
    #Setup all the parameters
    chopobject.setParms({"targetpath":node_path,"compute": 6,"start":start,"end":end,"units":0,"export":new_node.path()})
    #Export the channel to object.
    chopobject.setExportFlag(1)

    #Start bakeing the channel to keyframe animation.Check help for parameter detail.
    for t in new_node.parmTuple("./t"):
        t.keyframesRefit(1, 0, 1, 1, 1, 1.0, 0, 1, start, end, hou.parmBakeChop.KeepExportFlag)
    
    for r in new_node.parmTuple("./r"):
        r.keyframesRefit(1, 0, 1, 1, 1, 1.0, 0, 1, start, end, hou.parmBakeChop.KeepExportFlag)

    #Unexport the chopnode
    chopobject.setExportFlag(0)


