#Name: bake_anim
#v1.0 2018_06_30 Author:wang xiaowei  Email:wangxiaowei@ckyhvfx.com
#Bake all the parameters with expression and animation.

range = hou.playbar.playbackRange()
start = range[0]
end = range[1]


sel_nodes=hou.selectedNodes()

#check if there is a node selected, if none, raise warning to let user select nodes first.
if sel_nodes == ():
    raise NameError('请先选择节点！')


for old_node in sel_nodes:

    #Bake all the animated parameters.
    for i in old_node.parms():
        if len(i.keyframes()) > 0:
            i.keyframesRefit(1, 0, 1, 1, 1, 1.0, 0, 1, start, end, hou.parmBakeChop.KeepExportFlag)
