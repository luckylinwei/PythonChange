__author__ = 'Lin'

'''
对生成的中间抽象语法树进行处理，包括设置节点的标识符id、获取节点集合、获取id到node的映射id_to_node和保存节点间的child_parent关系等
'''

from collections import deque


# 以广度优先的顺序为每个节点设置标识符id
def id_set(tree_head):
    queue = deque()
    queue.append(tree_head)
    count = 0  # 用于设置id
    while len(queue) != 0:
        a = queue.popleft()
        a.id = count
        count += 1
        if a.children:
            for child in a.children:
                queue.append(child)


# 获取以node为根的子树中，所有节点的集合node_list，包括node本身，同时返回中间节点inner_node_list和叶子节点集合leaf_node_list
def node_get(node):
    leaf_node_list = []
    inner_node_list = []
    node_list = []
    queue = deque()
    queue.append(node)
    while len(queue) != 0:
        a = queue.popleft()
        if a.children:
            inner_node_list.append(a)
            node_list.append(a)
            for child in a.children:
                queue.append(child)
        else:
            leaf_node_list.append(a)
            node_list.append(a)
    return node_list, inner_node_list, leaf_node_list


# 字典id_to_node保存id到node的映射，key为节点id，value为id对应的节点Node
def id_to_node_get(node_list):
    keys = []
    values = []
    for node in node_list:
        keys.append(node.id)
        values.append(node)
    id_to_node = dict(zip(keys, values))
    return id_to_node


# 保存节点间的child_parent关系，形式为元组(child.id, parent.id)
def child_parent_information(tree_head):
    child_to_parent = []
    queue = deque()
    queue.append(tree_head)
    while len(queue) != 0:
        a = queue.popleft()
        if a.id == 0:
            child_to_parent.append((a.id, 'head_parent'))
        if a.children:
            for child in a.children:
                queue.append(child)
                child_to_parent.append((child.id, a.id))
    return child_to_parent


# 广度优先遍历
def breadth_first_traversal(node):
    queue = deque()
    queue.append(node)
    while len(queue) != 0:
        a = queue.popleft()
        print(a.label, a.value, 'matched: ', a.matched, 'id: ', a.id, 'parent: ', a.parent)
        if a.children:
            for child in a.children:
                queue.append(child)


# 广度优先遍历，结果保存在文件breadth_first_traversal.txt中
def breadth_first_traversal_tofile(node, filename):
    f = open(filename, 'w')
    queue = deque()
    queue.append(node)
    while len(queue) != 0:
        a = queue.popleft()
        print((a.label, a.value, 'matched: ', a.matched, 'id: ', a.id), file=f)
        if a.children:
            for child in a.children:
                queue.append(child)
    f.close()