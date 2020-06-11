# _*_ coding utf-8 _*_
'''
功能：
1，读取语料库问题句子，通过SIF算法计算每个句子的句向量
2，将‘问题句子：句向量’保存到本地文件
'''
from get_sent2vec import get_sent_vec
import pandas as pd
# 读取语料库中的所有问题句子
data = pd.read_csv('../data/dataset.csv', encoding='utf-8')
data.drop(data.index[32524:32526], inplace=True)  # 清除最后两行问题为数字的情况
question_lst = (data['question'].astype(str)).tolist()  # 强制转换类型，避免调用jieba出错，否则会报编码错误

# 准备空列表，用来保存通过SIF计算的’句子：向量‘字典
question2vec_dic_lst = []
for i in range(len(question_lst)):
    question2vec_dic_lst.append(get_sent_vec(question_lst[i].split()))  # 读取question列表中的每个句子时稍作处理，保证字符串的连贯
# print(question2vec_dic_lst)

# 将保存有’句子：向量‘的列表写入本地文件
save_question2vec = open('question2vec_pair.txt', 'w', encoding='utf-8')
for i in range(len(question_lst)):
    for key in question2vec_dic_lst[i]:
        # 将原向量列表的中括号去除，原本句向量每四个元素有一个换行，也去除，加换行符，按行保存每个’问题：向量‘对
        save_question2vec.writelines(key + '->' + str((question2vec_dic_lst[i][key])).strip('[').strip(']').replace('\n', ' ') + '\n')
save_question2vec.close()
