__author__ = 'Lin'

'''
Input：两个py文件left_filename和right_filename
Output：ChangeType的统计分布情况change_type_percentage
step1：写变更结果文件头
step2：输入更改前后的两个文件，调用code_change_extraction抽取变更
step3：将变更结果写入ChangeType_Extraction_File.csv
'''


import time
import csv
import os
from change_type import change_type_enum
from change_extraction import code_change_extraction


# 写变更结果文件头，w表示写文本文件，wb写二进制文件，a追加写文件
csvfile = open('ChangeType_Extraction_File.csv', 'w', newline='')  # 设置newline参数，去掉输出中的空行
csvwriter = csv.writer(csvfile, dialect='excel')
change_type = change_type_enum()
change_type.insert(0, 'left_file_name')  # 利用insert方法插入数据到列表中，便于以一行的方式写入csv文件
change_type.insert(1, 'right_file_name')
csvwriter.writerow(change_type)  # writerow写入一行数据，writerows写入多行数据
csvfile.close()


# 输入被比较的两个文件名
start = time.clock()
left_filename = 'scipy-0.16.0\scipy\linalg\_expm_frechet.py'
right_filename = 'scipy-0.16.1\scipy\linalg\_expm_frechet.py'


# 对相同路径下的两个文件进行比较
csvfile = open('ChangeType_Extraction_File.csv', 'a', newline='')  # 设置newline参数，去掉输出中的空行
csvwriter = csv.writer(csvfile, dialect='excel')
change_type_percentage = code_change_extraction(left_filename, right_filename)
change_type_percentage.insert(0, os.path.basename(left_filename))
change_type_percentage.insert(1, os.path.basename(right_filename))
csvwriter.writerow(change_type_percentage)
csvfile.close()

end = time.clock()
print('time: %fs' % (end - start))