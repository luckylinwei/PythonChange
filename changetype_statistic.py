__author__ = 'Dei'


'''
:param change_type_list是抽取的ChangeType集合
:return 返回的change_type_dict是一个字典，key为ChangeType，value为该种ChangeType在change_type_list中出现的次数，初始化为0
'''


from change_type import change_type_enum


# 根据变更抽取结果统计ChangeType的分布情况
def changetype_statistic(change_type_list):
    change_type = change_type_enum()  # change_type中存储了所有能识别的ChangeType
    value = [0] * len(change_type)
    change_type_dict = dict(zip(change_type, value))
    for change_type in change_type_list:
        change_type_dict[change_type] += 1  # 统计change_type_list中每种change_type出现的次数
    return change_type_dict