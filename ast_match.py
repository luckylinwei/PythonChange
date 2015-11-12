__author__ = 'Lin'

'''
实现两棵抽象语法树的匹配
匹配叶子节点时，采用双向最优匹配原则，在所有相似度大于阈值的叶子节点对中选择相似度最大的一组，加入匹配集合match_final
匹配中间节点时，采用first match
'''

from ngrams import string_similarity_ngram
from ast_information_process import node_get
import operator


# 匹配叶子节点
# 遍历T1和T2的叶子节点,将所有相似度值大于阈值的叶子节点对(left.id, right.id)加入集合match_temp
# value相似度使用ngrams计算
def leaf_match(left_leaf_node_list, right_leaf_node_list, f):
    match_temp = []
    for i in range(len(left_leaf_node_list)):
        for item in right_leaf_node_list:
            if left_leaf_node_list[i].label == item.label:
                sim = string_similarity_ngram(left_leaf_node_list[i].value, item.value, 2)
                if sim > f:
                    match_temp.append((left_leaf_node_list[i].id, item.id, sim))
    return match_temp


# 实现双向匹配，对match_temp按相似度大小降序排列，将相似度最大的叶子节点对(x,y)加入匹配集合match_final中
# 同时将match_temp中其余包含x或y节点信息的叶节点对删除，并将x、y标记为matched
def best_match(match_temp):
    # operator.itemgetter(2)用于获取对象第三维的数据(即相似度)，作为排序关键字
    match_temp.sort(key=operator.itemgetter(2), reverse=True)
    tag_list1 = []
    tag_list2 = []
    match_final = []
    for item in match_temp:
        if item[0] not in tag_list1 and item[1] not in tag_list2:
            match_final.append(item)
            tag_list1.append(item[0])
            tag_list2.append(item[1])
    return match_final


# 将match_final中的叶子节点matched标志置为1
def leaf_matched_set(left_leaf_node_list, right_leaf_node_list, match_final):
    for node in left_leaf_node_list:
        for pair in match_final:
            if node.id == pair[0]:
                node.matched = 1
    for node in right_leaf_node_list:
        for pair in match_final:
            if node.id == pair[1]:
                node.matched = 1


# 中间节点匹配
# 考虑阈值t的动态变化和叶子节点的权重
def inner_node_match(node1, node2, match_final, f, t):
    if node1.label == node2.label:
        common = 0  # 记录以node1为根的子树和以node2为根的子树中，匹配的叶子节点数
        node_list1, inner_node_list1, leaf_node_list1 = node_get(node1)
        node_list2, inner_node_list2, leaf_node_list2 = node_get(node2)
        for node in leaf_node_list1:
            if node.matched == 0:  # 若该叶子节点不存在与之匹配的节点，跳过
                continue
            else:
                id1 = node.id
                for item in match_final:  # 在match_final中找node的匹配信息，计算common
                    if item[0] == id1:
                        id2 = item[1]
                        for leaf_node in leaf_node_list2:
                            if leaf_node.id == id2:
                                common += 1
        max_num = len(leaf_node_list1) if len(leaf_node_list1) > len(leaf_node_list2) else len(leaf_node_list2)
        # 阈值t的大小根据子树规模动态改变
        if len(leaf_node_list1) <= 4 or len(leaf_node_list2) <= 4:
            t = 0.4
        sim_inner = common / max_num  # 好像没有int/double的问题
        sim_value = string_similarity_ngram(node1.value, node2.value, 2)
        # 为中间节点相似度设置权重，common leaves function有更高的权重
        # 即使中间节点value的相似度小于阈值f，但是若子树相似度远大于t，也认为两个中间节点相似
        if sim_inner >= 0.8:
            match_final.append((node1.id, node2.id, sim_value))
            node1.matched = 1
            node2.matched = 1
        elif sim_inner > t and sim_value > f:
            match_final.append((node1.id, node2.id, sim_value))
            node1.matched = 1
            node2.matched = 1