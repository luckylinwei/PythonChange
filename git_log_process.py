# -*- coding:utf-8 -*-
__author__ = 'Lin'

'''
处理Git的log信息，分析每次commit修改的python文件
commit_id用于记录ID号，modified用于标记本次commit是否修改了python文件
按行处理log信息，对于包含'commit'的行，若modified标记位为1，说明上次commit修改了python文件，保存到final_modified列表中，清空temp列表
若modified为0，说明上次commit未修改python文件，跳过；
处理完'commit'行后，记录新的commit_id
对于包含'.py'的行，记录被修改的文件名到temp_modified列表中，并将modified置1

比较某次commit修改的文件的前后两个版本，需要使用git的checkout命令撤销某次commit的修改
这里使用了subprocess.getstatusoutput与系统命令进行交互，当然首先要将Git加入系统Path，确保系统cmd能调用Git命令
'''

import re
import subprocess
import os
import csv
import time
from change_type import change_type_enum
from change_extraction import code_change_extraction


# 对git的log文件进行分析，返回每次commit的ID和本次commit修改的文件列表
def log_file_process(logfile):
    # 打开log文件会遇到'gbk'编码的问题，将open的编码方式显式声明为utf-8
    f = open(logfile, 'r', encoding='utf-8')
    lines = f.readlines()
    commit_id = ''
    modified = 0  # 标记一次commit是否有修改python文件
    temp_modified_file_list = []  # 保存一次commit修改的python文件
    final_modified_file_list = []  # 保存所有commit修改的python文件
    for line in lines:
        if 'commit' in line:  # 处理到包含commit的行时，根据modified标志位判断上次commit是否修改了python文件
            if modified == 1:
                for file in temp_modified_file_list:
                    final_modified_file_list.append((commit_id, file))
                temp_modified_file_list = []
                modified = 0
            result = re.findall('commit\s(.*)', line)  # 用正则表达式匹配获取commit ID
            if len(result) != 0:
                commit_id = result[0]
        if '.py' in line:  # 处理到包含.py的行时，将被修改文件加入temp_modified_file_list列表
            result = re.findall('\S+', line)
            temp_modified_file_list.append(result[0])
            modified = 1
    return final_modified_file_list


start = time.clock()
# 写变更结果文件头，w表示写文本文件，wb写二进制文件，a追加写文件
csvfile = open('ChangeType_Extraction_File.csv', 'w', newline='')  # 设置newline参数，去掉输出中的空行
csvwriter = csv.writer(csvfile, dialect='excel')
change_type = change_type_enum()
change_type.insert(0, 'Commit_ID')  # 利用insert方法插入数据到列表中，便于以一行的方式写入csv文件
change_type.insert(1, 'Changed_Filename')
csvwriter.writerow(change_type)  # writerow写入一行数据，writerows写入多行数据
csvfile.close()


# 对Git库的log文件进行处理，得到每次commit修改的python文件列表
final_modified_file_list = log_file_process('nameonly.txt')


# 用git的check out命令还原commit之前的文件，对更改前后的两个文件进行比较
unchanged_file_dir = 'E:\\PyCharm Workspace\\Change Extraction\\numpy-master'
changed_file_dir = 'E:\\PyCharm Workspace\\Change Extraction\\gitnumpy'
csvfile = open('ChangeType_Extraction_File.csv', 'a', newline='')  # 设置newline参数，去掉输出中的空行
csvwriter = csv.writer(csvfile, dialect='excel')
# 初始化Git repository，便于后续调用checkout命令(告诉程序对哪个库执行checkout命令)
subprocess.getstatusoutput('git init')
count = 0
for i in range(len(final_modified_file_list)):
    commit_id = final_modified_file_list[i][0]
    filename = final_modified_file_list[i][1]
    print(count, commit_id)
    count += 1
    subprocess.getstatusoutput('git checkout ' + commit_id + ' ' + filename)
    changed_file = os.path.join(changed_file_dir, filename)
    unchanged_file = os.path.join(unchanged_file_dir, filename)
    # 有可能出现增加或删除某个文件的操作，故对每个"文件"是否是文件进行判断
    if os.path.isfile(changed_file) and os.path.isfile(unchanged_file) and \
            changed_file.endswith('.py') and unchanged_file.endswith('.py'):
        print(filename)
        change_type_percentage = code_change_extraction(changed_file, unchanged_file)
        change_type_percentage.insert(0, os.path.basename(commit_id))
        change_type_percentage.insert(1, filename)
        csvwriter.writerow(change_type_percentage)
csvfile.close()

end = time.clock()
print('time: %fs' % (end - start))