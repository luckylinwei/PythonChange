__author__ = 'Lin'

'''
根据T1与T2的匹配节点集合match_final计算从T1转换为T2的编辑操作
编辑操作的计算：
    1. 遍历右子树，1）节点x在左子树中没有对应的匹配节点，则定义一个插入操作插入节点x；
                  2）若节点x在左子树中的匹配节点w存在，比较value(x)与value(y)是否相同，判断x的值是否发生了更新操作；
                                                    假设x的父节点为y，其匹配节点w的父节点为v，如果v与y不匹配，则认为x的父节点发生了变化，即x发生了移动；
    2. 遍历左子树，对于左子树中的节点，若在右子树中无匹配节点，则定义一个删除操作；
编辑操作的表示：
    插入：INS((x.label, x.value, x.id), z.label, z.id) x为新插入节点，z为插入节点的父节点
    更新：UPD((w.label, w.value, w.id), x.value) 表示节点w的值被更新为x.value
    移动：MOV((w.label, w.value, w.id), z.label, z.id) 表示节点w被移动到了z的孩子节点处
    删除：DEL((left_node.label, left_node.value, left_node.id)) 表示删除左子树上的left_node节点
其中：只有插入操作实际作用于T1，其余操作只是添加到edit_script列表中；插入新节点后，注意新节点与右子树中对应节点的匹配情况
     插入和删除操作以子树为单位，例如，若插入的是某个中间节点，则代表整棵子树的插入，子树中其余节点不再单独插入
change_information以元组(operation, changed_node, parent_node)的形式保存树的变更信息，用于将编辑操作与change type相对应
change_information1保存了插入、删除和更新操作的信息，change_information2保存的是移动操作的信息
'''


from intermediate_ast_build import Node
from ast_information_process import node_get


def editscript_calculate(left_node_list, match_final, left_id_to_node, right_id_to_node, right_node_list):
    left = []
    right = []
    for item in match_final:
        left.append(item[0])
        right.append(item[1])
    # 根据match_final得到两个匹配映射map_left_to_right和map_right_to_left
    # map_left_to_right为左树到右树的匹配情况，key为T1中的节点id，value为该节点在T2中的最佳匹配节点id
    map_left_to_right = dict(zip(left, right))
    map_right_to_left = dict(zip(right, left))

    num_of_node = len(left_node_list)  # 计算左子树节点数量，用于为新插入节点设置id
    edit_script = []
    change_information = []  # 记录插入、删除和更新等操作的信息
    change_information2 = []  # 记录移动操作的信息，MOV操作需要记录变化前后的父节点类型
    # 对于T2中的每个节点x,其父节点为y；x在T1中的匹配节点为w，y为z
    for right_node in right_node_list:
        x = right_node.id  # x、y、w和z都是id
        y = right_node.parent
        w = map_right_to_left.get(x)
        z = map_right_to_left.get(y)
        if x == 0:  # 跳过头指针
            continue
        else:
            x_node = right_id_to_node.get(x)
            z_node = left_id_to_node.get(z)
            # 如果x的匹配节点不存在且x未经过插入操作处理，则定义x为新增节点，创建一个插入操作INS(x,z)，表示在z节点上添加了节点x
            if w is None and right_node.inserted == 0:
                new_node = Node(x_node.label, x_node.value)  # 将插入操作作用于T1
                z_node.insertchild(new_node)
                new_node.id = num_of_node  # 保持左子树中原有节点id不变，为新插入的节点设置id
                map_right_to_left[x] = new_node.id  # 为新插入的节点设置匹配关系(x, z)
                map_left_to_right[new_node.id] = x
                left_id_to_node[num_of_node] = new_node  # 为新插入的节点设置id_to_node的匹配关系
                # 获取以x_node为根的子树中的所有节点集合node_list，将node_list集合中的节点标记为已插入node.inserted=1
                new_node.inserted = 1
                node_list, inner_node_list, leaf_node_list = node_get(x_node)
                for item in node_list:
                    item.inserted = 1
                operation = '(' + str((x_node.label, x_node.value, new_node.id)) + ', ' + str((z_node.label, z)) + ')'
                edit_script.append('INS ' + operation)  # 没考虑是在z节点的哪个位置上添加了节点x
                change_information.append(('INS', new_node, z_node))
                num_of_node += 1
            # 如果x的匹配节点存在，且未经过插入操作处理
            elif w is not None and right_node.inserted == 0:
                w_node = left_id_to_node.get(w)
                v_id = w_node.parent
                v_node = left_id_to_node.get(v_id)
                v_match = map_left_to_right.get(v_id)

                if w_node.value != x_node.value:  # 如果w节点存在，但其值不等于x节点的值，则定义一个更新操作UPD(w,value(x))
                    operation = '(' + str((w_node.label, w_node.value, w)) + ', ' + x_node.value + ')'
                    edit_script.append('UPD ' + operation)
                    change_information.append(('UPD', w_node, v_node))

                # v为w节点的父节点，如果v与y不匹配，判断x的父节点发生了变化，则定义一个移动操作MOV(w,z),表示w节点被移动到z节点下
                if v_match != y:
                    operation = '(' + str((w_node.label, w_node.value, w)) + ', ' + str((z_node.label, z_node.id)) + ')'
                    edit_script.append('MOV ' + operation)
                    # w_node为变更节点，v_node为变更节点父节点，z_node为移动后的父节点
                    change_information2.append(('MOV', w_node, v_node, z_node))

    # 遍历T1中的节点，如果某T1中的节点在T2中找不到对应的匹配节点，则定义一个删除操作DEL(w)
    # left_node_list中的节点按广度优先遍历的顺序存放
    for left_node in left_node_list:
        if map_left_to_right.get(left_node.id) is None and left_node.deleted == 0:
            left_node.deleted = 1
            node_list, inner_node_list, leaf_node_list = node_get(left_node)
            # 删除某个中间节点后，以该节点为根的子树都删除
            # 对节点left_node执行DEL操作，并获取以该节点为根的子树中的所有节点集合node_list，将node_list集合中的节点标记为已删除node.deleted=1
            for item in node_list:
                item.deleted = 1
            operation = '(' + str((left_node.label, left_node.value, left_node.id)) + ')'
            edit_script.append('DEL' + operation)
            # 找到被删除节点的父节点
            left_node_parent = left_id_to_node.get(left_node.parent)
            change_information.append(('DEL', left_node, left_node_parent))
    return edit_script, change_information, change_information2