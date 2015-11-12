__author__ = 'Lin'


'''
:param left_file和right_file是被比较的两个源文件
:return 表示ChangeType分布情况的列表change_type_percentage，change_type_percentage[i]表示第i种ChangeType出现的频率
step1：对输入的两个源程序进行处理，生成各自的中间抽象语法树，获取节点列表和id_to_node等信息
step2：根据匹配算法对叶子节点和中间节点进行匹配
step3：由节点匹配集合match_final计算从T1转换为T2的编辑操作
step4：将编辑操作与ChangeType一一对应
step5：对变更抽取结果进行统计分析，得到ChangeType的分布情况
'''


import customast
from intermediate_ast_build import ast_process, Node, Tree
from ast_information_process import id_set, node_get, child_parent_information, id_to_node_get
from ast_match import leaf_match, best_match, leaf_matched_set, inner_node_match
from edit_script import editscript_calculate
from editscript_changetype import changetype_generation
from change_type import change_type_enum
from changetype_statistic import changetype_statistic


def code_change_extraction(left_file, right_file):
    # 对两个源程序进行处理，生成各自的中间抽象语法树，并获取节点列表等相应信息
    left_AstContent = customast.parse_file(left_file)
    left_tree = Tree('头指针', 'left_head')
    left_root = Node('AstRoot', 'root')
    left_tree.linktohead(left_root)
    ast_process(left_AstContent, left_root)
    id_set(left_tree.head)
    left_child_to_parent = child_parent_information(left_tree.head)
    left_node_list, left_inner_node_list, left_leaf_node_list = node_get(left_tree.head)
    left_id_to_node = id_to_node_get(left_node_list)
    # 设置每个节点的parent_id属性
    for pair in left_child_to_parent:
        for left_id in left_id_to_node:
            if left_id == pair[0]:
                left_node = left_id_to_node.get(left_id)
                left_node.parent = pair[1]

    right_AstContent = customast.parse_file(right_file)
    right_tree = Tree('头指针', 'right_head')
    right_root = Node('AstRoot', 'root')
    right_tree.linktohead(right_root)
    ast_process(right_AstContent, right_root)
    id_set(right_tree.head)
    right_child_to_parent = child_parent_information(right_tree.head)
    right_node_list, right_inner_node_list, right_leaf_node_list = node_get(right_tree.head)
    right_id_to_node = id_to_node_get(right_node_list)
    for pair in right_child_to_parent:
        for right_id in right_id_to_node:
            if right_id == pair[0]:
                right_node = right_id_to_node.get(right_id)
                right_node.parent = pair[1]

    # 匹配叶子节点
    match_temp = leaf_match(left_leaf_node_list, right_leaf_node_list, 0.6)
    match_final = best_match(match_temp)
    leaf_matched_set(left_leaf_node_list, right_leaf_node_list, match_final)

    # 匹配中间节点
    # 对T1中所有标记为unmatched的中间节点，如果T2中存在一个节点y与之匹配，则将(x, y)加入match_final集合
    # 在匹配中间节点时采用first match，对于中间节点而言，first is best的概率较大
    for node1 in left_inner_node_list:
        for node2 in right_inner_node_list:
            if node1.matched == 0 and node2.matched == 0:
                inner_node_match(node1, node2, match_final, 0.4, 0.6)

    # 将头指针和根节点加入match_final集合，并将matched标志置为1，确保头指针和根节点一定匹配
    match_final.append((0, 0, 1.0))
    match_final.append(('head_parent', 'head_parent', 1.0))
    match_final.append((1, 1, 1.0))

    # 根据T1与T2的匹配节点集合match_final计算从T1转换为T2的编辑操作
    edit_script, change_information, change_information2 = \
        editscript_calculate(left_node_list, match_final, left_id_to_node, right_id_to_node, right_node_list)

    # 根据编辑操作得到相应的ChangeType
    change_type_list, scc_list, parent_entity_list, changed_entity_list = \
        changetype_generation(change_information, change_information2)
    '''
    # 输出change信息
    for i in range(len(change_type_list)):
        if change_type_list[i] != '':
            print('\nChangeType:', change_type_list[i])
            print('scc:', scc_list[i])
            print('ChangedEntity:', changed_entity_list[i])
            print('ParentEntity:', parent_entity_list[i])
    '''
    # 根据变更抽取结果统计ChangeType的分布
    change_type = change_type_enum()
    change_type_percentage = [0] * len(change_type)  # 用于保存每种change出现的百分比
    # 若change_type_list长度为0，表示没有不同，change_type_percentage中的元素全为0，否则计算每种change出现的频率
    change_type_dict = changetype_statistic(change_type_list)
    if len(change_type_list) != 0:
        for key, value in change_type_dict.items():
            for i in range(len(change_type)):
                if key == change_type[i]:
                    change_type_percentage[i] = value / len(change_type_list)

    # change_type_percentage在对应位置保存了每种change_type的分布百分比
    # 例如，change_type_percentage[i]保存的是change_type[i]出现的频率
    return change_type_percentage