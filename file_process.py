__author__ = 'Lin'

'''
step1：对两个版本程序的源文件进行处理，获取两个目录下的所有py文件
step2：对于版本1中的所有文件，找到版本2中与其对应的文件，返回文件列表。所谓对应，是指在版本名之后的所有路径和文件名都一致
例如，我们认为v1.0\a\b\c.py和v2.0\a\b\c.py对应
'''


import os


left_pyfile_list = []
right_pyfile_list = []


# 遍历left目录，获取其中所有的py文件，保存在left_pyfile_list中
def scandir_left(filedir):
    for file in os.listdir(filedir):
        # isfile()和isdir()在测试时必须使用绝对路径，os.path.join()函数能自动将需要的路径连接起来得到绝对路径
        fullpath = os.path.join(filedir, file)
        if os.path.isfile(fullpath) and fullpath.endswith('.py'):
            left_pyfile_list.append(fullpath)
        if os.path.isdir(fullpath):
            scandir_left(fullpath)


# 遍历right目录，获取其中所有的py文件，保存在right_pyfile_list中
def scandir_right(filedir):
    for file in os.listdir(filedir):
        fullpath = os.path.join(filedir, file)
        if os.path.isfile(fullpath) and fullpath.endswith('.py'):
            right_pyfile_list.append(fullpath)
        if os.path.isdir(fullpath):
            scandir_right(fullpath)


# 对于left_filename中的所有文件，找right_filename中与其对应的文件，返回文件列表
def file_find(filedir, left_filename, right_filename):
    left_filepath = os.path.join(filedir, left_filename)
    scandir_left(left_filepath)  # 获取left_filepath目录下的所有python文件
    right_filepath = os.path.join(filedir, right_filename)
    scandir_right(right_filepath)
    left = []  # right对应位置保存了用来与left比较的文件
    right = []
    for left_file in left_pyfile_list:
        for right_file in right_pyfile_list:
            # 去掉filedir和filename部分比较，但保存的是绝对路径。要求被比较的两个文件从源程序名之后都一样
            if right_file[len(right_filepath) + 1:] == left_file[len(left_filepath) + 1:]:
                left.append(left_file)
                right.append(right_file)
    return left, right