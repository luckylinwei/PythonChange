__author__ = 'Lin'

'''
分析parse后的AstContent，对Class、Function等结构进行处理，生成中间抽象语法树
'''

import re
import string
import ast
import astunparse


# 中间抽象语法树节点类
class Node:
    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.children = []  # 用list存放多个孩子节点
        self.matched = 0  # 用于标记节点是否匹配，初始化matched=0,不匹配
        self.id = 0  # 为每个节点设置标识符，用于后续匹配，初始化为0
        self.deleted = 0  # 标记该节点是否被删除，默认为未删除0
        self.inserted = 0  # 标记该节点是否被插入，默认为未插入0
        self.parent = 0  # 记录父节点的id

    def insertchild(self, node):
        self.children.append(node)  # 插入孩子节点


# 多叉树
class Tree:
    def __init__(self, label, value):
        self.head = Node(label, value)

    def linktohead(self, node):
        self.head.insertchild(node)


# 字符串处理，过滤string中的whitespace，包括回车换行空格等，用法：pattern.sub('', string)
pattern = re.compile('(%s)' % ('|'.join([c for c in string.whitespace])))


# 处理ast中的每个结构astbody，生成节点Node，插入以parent为根的子树中
# 对于If.body等无法直接处理的结构，利用unparse-parse的方法重新生成新的AST进行处理
def ast_process(astbody, parent):
    for child in ast.iter_child_nodes(astbody):
        if isinstance(child, ast.Assign):
            label = 'Assign'
            value = astunparse.unparse(child)
            value = pattern.sub('', value)  # 字符串处理
            node_assign = Node(label, value)
            parent.insertchild(node_assign)

        if isinstance(child, ast.Break):
            label = 'Break'
            value = 'break'
            node_break = Node(label, value)
            parent.insertchild(node_break)

        if isinstance(child, ast.Expr):
            # 处理表达式中的特殊类型：Call
            if isinstance(child.value, ast.Call):
                label = 'Call'
                value = astunparse.unparse(child.value)
                value = pattern.sub('', value)
                node_call = Node(label, value)
                parent.insertchild(node_call)
                '''
            # 处理yield
            elif isinstance(child.value, ast.Yield):
                label = 'Yield'
                yeild_value = child.value
                value = astunparse.unparse(yeild_value.value)
                value = pattern.sub('', value)
                node_yield = Node(label, value)
                parent.insertchild(node_yield)
                '''
            else:
                label = 'Expr'
                value = astunparse.unparse(child)
                value = pattern.sub('', value)
                node_expr = Node(label, value)
                parent.insertchild(node_expr)

        if isinstance(child, ast.AugAssign):
            label = 'AugAssign'
            value = astunparse.unparse(child)
            value = pattern.sub('', value)
            node_augassign = Node(label, value)
            parent.insertchild(node_augassign)

        if isinstance(child, ast.Return):
            node_return = Node('Return', 'return')
            parent.insertchild(node_return)
            # 如果有返回值，对返回值进行处理
            if child.value:
                return_value = astunparse.unparse(child.value)
                return_value = pattern.sub('', return_value)
                if return_value[0] == '(' and return_value[-1] == ')':
                    return_value = return_value[1:-1]  # 去掉首尾的括号
                return_value = return_value.split(',')
                for item in return_value:
                    node_return_value = Node('Return_Value', item)
                    node_return.insertchild(node_return_value)

        if isinstance(child, ast.If):
            label = 'If'
            value = astunparse.unparse(child.test)  # If节点的value为其判断条件
            value = pattern.sub('', value)
            node_if = Node(label, value)
            parent.insertchild(node_if)

            # 如果If包含oreles块,则生成Then和Else作为If的子节点，否则body的内容直接作为If的孩子节点插入
            if child.orelse:
                node_then = Node('Then', value)  # 自身不带value的节点从其父节点继承value
                node_if.insertchild(node_then)
                source_then = astunparse.unparse(child.body)  # If.body无法直接处理，先反解析为源代码，再重新生成ast
                ast_then = ast.parse(source_then)
                ast_process(ast_then, node_then)

                node_else = Node('Else', value)
                node_if.insertchild(node_else)
                source_else = astunparse.unparse(child.orelse)
                ast_else = ast.parse(source_else)
                ast_process(ast_else, node_else)
            else:
                source_body = astunparse.unparse(child.body)  # If.body无法直接处理，先反解析为源代码，再重新生成ast
                ast_then = ast.parse(source_body)
                ast_process(ast_then, node_if)

        if isinstance(child, ast.FunctionDef):
            value = child.name
            value = pattern.sub('', value)
            label = 'FunctionDef'
            node_functiondef = Node(label, value)
            parent.insertchild(node_functiondef)
            # 处理FunctionDef的参数和装饰器decorator_list，参数分为位置参数args、可变长度参数vararg和关键字参数kwargs几类
            source_args = astunparse.unparse(child.args)
            source_args = pattern.sub('', source_args)  # 过滤source_args中的空格、回车等
            # source_args = source_args.split(",")  # 将参数按逗号划分
            args = []  # 位置参数
            vararg = []  # 可变长度位置参数*args
            kwonlyargs = []  # 关键字参数
            kwargs = []  # 可变长度关键字参数**args
            defaults = []  # 默认位置参数
            kw_defaults = []  # 默认关键字参数
            varargs_flag = 0  # 用于标记是否已处理varargs，以区别args和kwonlyargs
            if source_args != "":  # 参数列表为空时，source_args为“ ”，经过pattern.sub后变为""，添加参数节点应当在参数列表不为空时处理
                source_args = source_args.split(",")  # 将参数按逗号划分
                for item in source_args:
                    if "**" in item:
                        kwargs.append(item[2:])
                    elif "*" in item:
                        vararg.append(item[1:])
                        varargs_flag = 1
                    elif "=" in item and varargs_flag == 1:
                        kw_defaults.append(item)
                    elif "=" not in item and varargs_flag == 1:
                        kwonlyargs.append(item)
                    elif "=" in item:
                        defaults.append(item)
                    else:
                        args.append(item)
            # 为args、vararg和kwarg等参数设置label和value，作为节点插入node_functiondef中
            for arg in args:
                arg_node = Node('args', arg)
                node_functiondef.insertchild(arg_node)
            for arg in vararg:
                vararg_node = Node('vararg', arg)
                node_functiondef.insertchild(vararg_node)
            for arg in kwonlyargs:
                kwonlyargs_node = Node('kwnolyarg', arg)
                node_functiondef.insertchild(kwonlyargs_node)
            for arg in kwargs:
                kwargs_node = Node('kwargs', arg)
                node_functiondef.insertchild(kwargs_node)
            for arg in defaults:
                defaults_node = Node('default_args', arg)
                node_functiondef.insertchild(defaults_node)
            for arg in kw_defaults:
                kw_defaults_node = Node('kw_default', arg)
                node_functiondef.insertchild(kw_defaults_node)
            # 处理decorator_list
            '''
            decorator_list = []
            if child.decorator_list:
                for decorator in child.decorator_list:
                    decorator_list.append(decorator.id)
            if len(decorator_list) != 0:
                for decorator in decorator_list:
                    decorator_node = Node('decorator', decorator)
                    node_functiondef.insertchild(decorator_node)
            '''
            # 处理Function_Body
            source_functionbody = astunparse.unparse(child.body)
            ast_functionbody = ast.parse(source_functionbody)
            ast_process(ast_functionbody, node_functiondef)

        if isinstance(child, ast.ClassDef):
            class_name = child.name
            label = 'ClassDef'
            node_classdef = Node(label, class_name)
            parent.insertchild(node_classdef)
            # 处理基类
            bases = astunparse.unparse(child.bases)  # 只考虑name和base，keywos,starargs等暂时不考虑
            bases = pattern.sub('', bases)
            if bases != '':  # 有基类的时候才处理
                node_bases = Node('base', bases)
                node_classdef.insertchild(node_bases)
            '''
            # 处理decorator_list
            decorator_list = []
            if child.decorator_list:
                for decorator in child.decorator_list:
                    decorator_list.append(decorator.id)
            if len(decorator_list) != 0:
                for decorator in decorator_list:
                    decorator_node = Node('decorator', decorator)
                    node_classdef.insertchild(decorator_node)
            '''
            # 处理class body
            source_classbody = astunparse.unparse(child.body)  # 同样对body做unparse -> parse处理
            ast_classbody = ast.parse(source_classbody)
            ast_process(ast_classbody, node_classdef)

        if isinstance(child, ast.For):
            label = 'For'
            value = astunparse.unparse(child.iter)  # For的value再考虑
            value = pattern.sub('', value)
            node_for = Node(label, value)
            parent.insertchild(node_for)
            # 判断For循环是否有else部分，如果有，new一个ForBody和ForElse作为Node_For的孩子节点；否则，for.body直接作为For的孩子节点插入
            if child.orelse:
                # 处理For.body
                node_then = Node('Then', value)
                node_for.insertchild(node_then)
                source_then = astunparse.unparse(child.body)
                ast_then = ast.parse(source_then)
                ast_process(ast_then, node_then)
                # 处理For.orelse
                node_else = Node('Else', value)
                node_for.insertchild(node_else)
                source_else = astunparse.unparse(child.orelse)
                ast_else = ast.parse(source_else)
                ast_process(ast_else, node_else)
            else:
                source_forbody = astunparse.unparse(child.body)
                ast_forbody = ast.parse(source_forbody)
                ast_process(ast_forbody, node_for)

        if isinstance(child, ast.While):
            label = 'While'
            value = astunparse.unparse(child.test)
            value = pattern.sub('', value)
            node_while = Node(label, value)
            parent.insertchild(node_while)
            source_whildbody = astunparse.unparse(child.body)
            ast_whilebody = ast.parse(source_whildbody)
            ast_process(ast_whilebody, node_while)