# _*_ coding utf-8 _*_
'''
功能：
1，调用get_sent2vec.py中的get_sent_vec()计算用户输入的问题的句向量
2，尝试计算用户问题句向量和所有句向量的距离，排序选前十
3，通过knn算法分两次计算距离，减小计算量，排序选前十
输入： 用户的问题句子
输出： 通过句向量相似性计算的前十个问题句子
'''
from get_sent2vec import get_sent_vec
from cosine_similarity import cosine_similarity

def sentvec_match(user_input):
    # 获取用户输入的问题句子，转换为列表，方便get_sent_vec()计算
    # usr_question = input('你好，我是小汤，请问有什么能帮助你的吗？\n')
    usr_question = user_input.strip().split()
    usr_question2vec = get_sent_vec(usr_question)
    # print(type(usr_question2vec), len(usr_question2vec[usr_question[0]]))

    # 读取所有语料库问题句向量文件，准备计算句向量相似性
    # 读取本地文件‘问题句子：句向量’，还原为可用的字典‘问题句子，句向量’
    with open('model/question2vec_pair.txt', encoding='utf-8') as f:
        question2vec_file = f.readlines()
    question2vec_dic = {}
    for i in question2vec_file:
        question2vec_dic[i.split('->')[0]] = list((float(x)
                                                for x in i.split('->')[1].split()))
    # print(dic['问题1'])
    # print(len(dic['问题1']))

    # 调用余弦相似度函数，计算句向量相似性，保存为‘问题句子：相似性’字典
    # 这一步花费时间10秒钟
    cosimilar_dic = {}
    for key in question2vec_dic:
        cosimilar_dic[key] = cosine_similarity(
            question2vec_dic[key], usr_question2vec[usr_question[0]])

    # 对‘问题句子：相似性’字典按value值排序，获取相似性高的前十个句子
    sorted_questions = sorted(cosimilar_dic.items(
    ), key=lambda kv: (kv[1], kv[0]), reverse=True)
    similar_question_lst = []
    for i in range(10):
        similar_question_lst.append(sorted_questions[i][0])

    # print(similar_question_lst)
    return similar_question_lst
