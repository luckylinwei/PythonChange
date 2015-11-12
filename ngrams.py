__author__ = 'Lin'

"""
String similarity measures using n-Grams, n-grams are bags and constructed by putting a sliding window of length n
over a string and extracting at each position the n underlying characters
:param str1 & str2: strings that will be calculated
:param param_N: the length of a sliding window over a string
"""

"""
split()划分字符串时包括前后空格，_split()划分时不包括。例如，
_split("happy")：['ha', 'ap', 'pp', 'py']
split("happy")：['$h', 'ha', 'ap', 'pp', 'py', 'y$']
我们采用正常的不带前后空格的_split()方法
为简单起见，将外部库ngram中的_split()方法重写为split方法
反正意思就是现在不调用外部库了
"""


def split(N, string):
    for i in range(len(string) - N + 1):
        yield string[i:i + N]


def string_similarity_ngram(str1, str2, param_N):
    if str1 == str2:
        ngram_similarity = 1.0
    # 字符串长度小于param_N时，无法实现n-grams划分，采用公式计算时会报除数为零的错误，故单独处理
    elif len(str1) < param_N or len(str2) < param_N:
        ngram_similarity = 0.0
    else:  # 以大小为param_N的活动窗口对字符串进行划分，items_sharing_ngrams()返回划分后的两个字符串中共同元素的个数
        list1 = list(split(param_N, str1))
        list2 = list(split(param_N, str2))
        len_of_str1 = len(list(list1))
        len_of_str2 = len(list(list2))
        common = 0
        for item in list2:
            if item in list1:
                common += 1
        ngram_similarity = 2 * common / (len_of_str1 + len_of_str2)  # n-grams similarity计算公式
    return ngram_similarity