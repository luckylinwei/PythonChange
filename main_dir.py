__author__ = 'Lin'

'''
Input：被比较的两个程序(源程序代码所在目录)
Output：每个文件的ChangeType的统计分布情况change_type_percentage
step1：写变更结果文件头
step2：输入两个版本源程序所在的目录，获取需要被比较的文件列表
step3：利用filecmp.cmp比较对应的两个源文件是否相同，对于发生change的文件调用code_change_extraction抽取变更
step4：将变更结果写入ChangeType_Extraction.csv
'''


import time
import filecmp
import csv
import os
from file_process import file_find
from change_type import change_type_enum
from change_extraction import code_change_extraction


# 写变更结果文件头，w表示写文本文件，wb写二进制文件，a追加写文件
csvfile = open('ChangeType_Extraction.csv', 'w', newline='')  # 设置newline参数，去掉输出中的空行
csvwriter = csv.writer(csvfile, dialect='excel')
change_type = change_type_enum()
change_type.insert(0, 'filename')  # 利用insert方法插入数据到列表中，便于以一行的方式写入csv文件
change_type.insert(1, 'filepath')
csvwriter.writerow(change_type)  # writerow写入一行数据，writerows写入多行数据
csvfile.close()


# 输入两个版本的文件所在目录,left和right列表中保存了用于比较的两个版本对应路径下的同名文件
start = time.clock()
filedir = 'E:\PyCharm Workspace\Change Extraction'
left_filename = 'scipy-0.16.0'
right_filename = 'scipy-0.16.1'
left, right = file_find(filedir, left_filename, right_filename)


# 对两个版本程序的对应源代码文件进行比较
csvfile = open('ChangeType_Extraction.csv', 'a', newline='')  # 设置newline参数，去掉输出中的空行
csvwriter = csv.writer(csvfile, dialect='excel')
count = 0  # 记录两个版本程序不同文件的数量
for i in range(len(left)):
    # 利用filecmp.cmp比较两个文件是否相同，不相同的用code_change_extraction抽取变更
    if filecmp.cmp(left[i], right[i]) is False:
        change_type_percentage = code_change_extraction(left[i], right[i])
        count += 1
        change_type_percentage.insert(0, os.path.basename(left[i]))
        change_type_percentage.insert(1, os.path.dirname(left[i]))
        csvwriter.writerow(change_type_percentage)


print('\nThere are %d different files between %s and %s ' % (count, left_filename, right_filename))
csvfile.close()
end = time.clock()
print('time: %fs' % (end - start))