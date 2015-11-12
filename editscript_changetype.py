__author__ = 'Dei'

'''
分别定义4个函数处理INS、UPD、MOV和DEL等4种编辑操作，得到每个变更操作对应的change type
函数changetype_generation：
:param change_information以元组(operation, changed_node, parent_node)的形式保存树的变更信息，根据operation的类型调用不同的函数进行处理，得到相应的ChangeType
:return change_type_list, scc_list, parent_entity_list, changed_entity_list
'''


# 定义函数分别处理INS、UPD、MOV和DEL等4种编辑操作，得到每个变更操作对应的change type
# 函数参数change_information为一个元组，以(operation, changed_node, parent_node)的形式保存树的变更信息
def insert_process(change_information_tuple):
    changed_node = change_information_tuple[1]
    changed_parent = change_information_tuple[2]
    change_type = 'Other Change Type'
    scc = 'Insert: ' + changed_node.value
    parent_entity = changed_parent.label + ': ' + changed_parent.value
    changed_entity = changed_node.label + ': ' + changed_parent.value
    label = changed_node.label
    if label == 'ClassDef':
        change_type = 'Additional Class'
    if label == 'base':
        change_type = 'Parent Class Insert'
    if label == 'decorator':
        change_type = 'Decorator Insert'
    elif label == 'FunctionDef':
        change_type = 'Additional Functionality'
    elif label == 'Assign' or label == 'Expr' or label == 'AugAssign' or label == 'Break':
        change_type = 'Statement Insert'
    elif label == 'Call':
        change_type = 'Method Call Insert'
    elif label == 'Yield':
        change_type = 'Yield Insert'
    elif label == 'If':
        change_type = 'If Insert'
    elif label == 'Else':
        change_type = 'Else Part Insert'
    elif label == 'While' or label == 'For':
        change_type = 'Loop Insert'
    elif label == 'args':
        change_type = 'Locational Parameter Insert'
    elif label == 'vararg':
        change_type = 'Variable Parameter Insert'
    elif label == 'kwnolyarg':
        change_type = 'Keyword Parameter Insert'
    elif label == 'kwargs':
        change_type = 'Variable Keyword Parameter Insert'
    elif label == 'default_args':
        change_type = 'Default Locational Parameter Insert'
    elif label == 'kw_defalut':
        change_type = 'Default Keyword Parameter Insert'
    elif label == 'Return_Value':
        change_type = 'ReturnValue Insert'
    elif label == 'Return':
        change_type = 'Return Insert'
    return change_type, scc, parent_entity, changed_entity


def delete_process(change_information_tuple):
    changed_node = change_information_tuple[1]
    changed_parent = change_information_tuple[2]
    scc = 'Delete: ' + changed_node.value
    parent_entity = changed_parent.label + ': ' + changed_parent.value
    changed_entity = changed_node.label + ': ' + changed_node.value
    change_type = 'Other Change Type'
    label = changed_node.label
    if label == 'ClassDef':
        change_type = 'Removed Class'
    if label == 'base':
        change_type = 'Parent Class Delete'
    if label == 'decorator':
        change_type = 'Decorator Delete'
    elif label == 'FunctionDef':
        change_type = 'Removed Functionality'
    elif label == 'Assign' or label == 'Expr' or label == 'AugAssign' or label == 'Break':
        change_type = 'Statement Delete'
    elif label == 'Call':
        change_type = 'Method Call Delete'
    elif label == 'Yield':
        change_type = 'Yield Delete'
    elif label == 'If':
        change_type = 'If Delete'
    elif label == 'Else':
        change_type = 'Else Part Delete'
    elif label == 'While' or label == 'For':
        change_type = 'Loop Delete'
    elif label == 'args':
        change_type = 'Locational Parameter Delete'
    elif label == 'vararg':
        change_type = 'Variable Parameter Delete'
    elif label == 'kwnolyarg':
        change_type = 'Keyword Parameter Delete'
    elif label == 'kwargs':
        change_type = 'Variable Keyword Parameter Delete'
    elif label == 'default_args':
        change_type = 'Default Locational Parameter Delete'
    elif label == 'kw_defalut':
        change_type = 'Default Keyword Parameter Delete'
    elif label == 'Return_Value':
        change_type = 'ReturnValue Delete'
    elif label == 'Return':
        change_type = 'Return Delete'
    return change_type, scc, parent_entity, changed_entity


# 保存move信息的change_information_tuple格式为('MOV', 变更节点w_node，变更节点父节点v_node，移动后的父节点z_node)
def move_process(change_information_tuple):
    changed_node = change_information_tuple[1]
    changed_parent = change_information_tuple[2]
    new_parent = change_information_tuple[3]
    scc = 'Move: ' + changed_node.value
    parent_entity = changed_parent.label + ': ' + changed_parent.value
    changed_entity = changed_node.label + ': ' + changed_parent.value
    change_type = 'Other Change Type'
    '''
    if label == 'Expr' or label == 'Assign' or label == 'AugAssign' or label == 'Break':
        # 如果变更实体的类型为语句，且MOVE操作后的父实体label value与原父实体相同，则判断变更为语句顺序改变
        # 这个有点不太明白，父节点发生了变化才归为MOV操作吧？所以MOV操作后的父实体label和value怎么会与原父实体相同？
       if changed_parent.label == new_parent.label and changed_parent.value == new_parent.value:
           change_type = 'Statement Ordering Change'
       # 如果父节点不同，则判断变更语句类型为父语句的变更
       else:
           change_type = 'Statement Parent Change'
    '''
    # 如果变更节点的父节点不同，则判断变更语句类型为Parent Change
    if changed_parent.label != new_parent.label or changed_parent.value != new_parent.value:
        change_type = 'Statement Parent Change'
    return change_type, scc, parent_entity, changed_entity


def update_process(change_information_tuple):
    changed_node = change_information_tuple[1]
    changed_parent = change_information_tuple[2]
    scc = 'Update: ' + changed_node.value
    parent_entity = changed_parent.label + ': ' + changed_parent.value
    changed_entity = changed_node.label + ': ' + changed_parent.value
    change_type = 'Other Change Type'
    label = changed_node.label
    if label == 'FunctionDef':
        change_type = 'Function Renaming'
    elif label == 'If' or label == 'For' or label == 'While' or label == 'Then':
        change_type = 'Conditional Expression Change'
    elif label == 'Expr' or label == 'Assign' or label == 'AugAssign' or label == 'Break':
        change_type = 'Statement Update'
    elif label == 'Call':
        change_type = 'Method Call Update'
    elif label == 'Yield':
        change_type = 'Yield Update'
    elif label == 'ClassDef':
        change_type = 'Class Renaming'
    elif label == 'base':
        change_type = 'Parent Class Update'
    elif label == 'args' or label == 'vararg' or label == 'kwnolyarg' or \
                    label == 'kwargs' or label == 'default_args' or label == 'kw_default':
        change_type = 'Parameter Renaming'
    return change_type, scc, parent_entity, changed_entity


# 判断change_information中每个元素的编辑操作类型，调用对应的函数处理，输出change_type信息
def changetype_generation(change_information, change_information2):
    change_type_list = []
    scc_list = []
    parent_entity_list = []
    changed_entity_list = []
    for change_information_tuple in change_information:
        if change_information_tuple[0] == 'INS':
            if change_information_tuple[1].label == 'AstRoot':  # 不考虑根节点的change type
                continue
            else:
                change_type, scc, parent_entity, changed_entity = insert_process(change_information_tuple)
                change_type_list.append(change_type)
                scc_list.append(scc)
                parent_entity_list.append(parent_entity)
                changed_entity_list.append(changed_entity)
        elif change_information_tuple[0] == 'DEL':
            if change_information_tuple[1].label == 'AstRoot':  # 不考虑根节点的change type
                continue
            else:
                change_type, scc, parent_entity, changed_entity = delete_process(change_information_tuple)
                change_type_list.append(change_type)
                scc_list.append(scc)
                parent_entity_list.append(parent_entity)
                changed_entity_list.append(changed_entity)
        elif change_information_tuple[0] == 'UPD':
            if change_information_tuple[1].label == 'AstRoot':  # 不考虑根节点的change type
                continue
            else:
                change_type, scc, parent_entity, changed_entity = update_process(change_information_tuple)
                change_type_list.append(change_type)
                scc_list.append(scc)
                parent_entity_list.append(parent_entity)
                changed_entity_list.append(changed_entity)
    # return change_type_list, scc_list, parent_entity_list, changed_entity_list
    # 插入操作作用在T1上会影响移动操作的判断，会把新插入的节点认为是移动操作；MOV对应的change type还不多，先放一放
    for change_information_tuple in change_information2:
        if change_information_tuple[1].label == 'AstRoot':  # 不考虑根节点的change type
                continue
        else:
            change_type, scc, parent_entity, changed_entity = move_process(change_information_tuple)
            change_type_list.append(change_type)
            scc_list.append(scc)
            parent_entity_list.append(parent_entity)
            changed_entity_list.append(changed_entity)
    return change_type_list, scc_list, parent_entity_list, changed_entity_list