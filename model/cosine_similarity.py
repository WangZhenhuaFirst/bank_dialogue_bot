# _*_ coding utf-8 _*_
'''
功能：
定义计算余弦相似度的函数
输入：两个向量（list），等长
输出：余弦相似度（-1,1），可以选择norm为True将余弦相似度归一化为（0,1）
'''
import numpy as np


def bit_product_sum(x, y):
    return sum([item[0] * item[1] for item in zip(x, y)])


def cosine_similarity(x, y, norm=False):
    """ 计算两个向量x和y的余弦相似度 """
    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    # f x == zero_list or y == zero_list:
    #    return float(1) if x == y else float(0)

    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内


if __name__ == '__main__':
    print(cosine_similarity([0, 0], [0, 0]))  # 1.0
    print(cosine_similarity([1, 1], [0, 0]))  # 0.0
    print(cosine_similarity([1, 1], [-1, -1]))  # -1.0
    print(cosine_similarity([1, 1], [2, 2]))  # 1.0
    print(cosine_similarity([3, 3], [4, 4]))  # 1.0
    print(cosine_similarity([1, 2, 2, 1, 1, 1, 0], [1, 2, 2, 1, 1, 2, 1]))  # 0.938194187433
