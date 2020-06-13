# _*_ coding utf-8 _*_
'''
功能：
1，设置参数，定义使用SIF算法计算句向量的函数，方便后续调用
输入： 问题语料库的所有问题句子，存为list类型，不使用stopwords
输出： ‘问题句子：句向量’，类型为字典
'''
# 调用SIF辅助函数及第三方库
import data_io
import params
import SIF_core
import os
import numpy as np
import pandas as pd
import re
from gensim.models import Word2Vec
import pdb

# 参数设置
# the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]
weightpara = 1e-3


# 词向量文件，词频文件，超参数设置
wordfile = 'data/word2vec_100d.txt'
weightfile = 'data/words_count.txt'


# 详见data_io.py
(words, We) = data_io.getWordmap(wordfile)
word2weight = data_io.getWordWeight(weightfile, weightpara)
weight4ind = data_io.getWeight(words, word2weight)


def get_sent_vec(sentences):
    '''
    通过SIF算法计算句向量
    :param sentences: 类型为列表，列表内的元素为字句子（句子类型为字符串，不用通过jieba.cut分词处理）
    :return: 输出类型为字典，key为句子字符串，value为句向量列表
    '''
    import params
    # 详见data_io.py
    x, m = data_io.sentences2idx(sentences, words)
    w = data_io.seq2weight(x, m, weight4ind)

    # 参数设置
    rmpc = 1  # number of principal components to remove in SIF weighting scheme
    params = params.params()
    params.rmpc = rmpc

    # 调用SIF核心算法计算句向量，详见SIF_core
    embedding = SIF_core.SIF_embedding(We, x, w, params)

    get_sent_vec = {}
    for i in range(len(embedding)):
        get_sent_vec[sentences[i]] = embedding[i]

    return get_sent_vec


if __name__ == '__main__':
    s = ['怎么办理银行卡']
    print(get_sent_vec(s))


