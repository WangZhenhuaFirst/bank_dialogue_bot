# _*_ coding utf-8 _*_
import jieba
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE
import random
from collections import Counter

from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec, word2vec, KeyedVectors
from gensim.models.word2vec import LineSentence

# 读取停用词表
stop_lst = []
with open("stopwords.txt", encoding='utf-8') as f:
    for line in f:
        stop_lst.append(line.strip())
f.close()

# 清洗数据，去掉停用词
def rmv_stopwords(sentences):
    clean_snts = []
    for word in jieba.cut(sentences):
        if word not in stop_lst:
            clean_snts.append()
    return clean_snts


# 分词
def cut2words(sentences):
    return " ".join(jieba.cut(sentences))


data = pd.read_csv("dataset.csv", encoding='utf-8')  # 读取银行业务问答语料
data.drop(data.index[32524:32526], inplace=True)
questions = (data['question'].astype(str)).tolist()
print(questions[0:30])

fileTrainSeg=[]
for i in range(len(questions)):
    fileTrainSeg.append(' '.join(list(jieba.cut(questions[i],cut_all=False))))
print(fileTrainSeg[0:30])

questions_seg = 'questions_seg.txt'
with open(questions_seg,'w',encoding='utf-8') as fW:
    for i in range(len(questions)):
        try:
            fW.write(str(' '.join(list(jieba.cut(questions[i])))))
            fW.write('\n')
        except:
            pass

whole_corpus = ''
for i in questions:
    try:
        whole_corpus += i
    except:
        pass
words_count = Counter(jieba.cut(whole_corpus))
words_count = words_count.most_common()

with open('words_count.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join('%s,%s' % x for x in words_count))

# ！！！！注意，生成本地词向量TXT文件后，打开文件删除首行的统计信息
path = get_tmpfile('word2vec_100d.model')
model = Word2Vec(LineSentence(questions_seg), size=100, min_count=3, workers=4)
model.save('word2vec_100d.model')
model.wv.save_word2vec_format('word2vec_100d.txt')




