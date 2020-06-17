import random
import pickle
import jieba

with open('data/stopwords.txt') as file:
        stopwords = file.read().split('\n')

with open('data/inverted_index.pickle', 'rb') as handle:
    word_docs_dict = pickle.load(handle)


def inverted_index_match(user_input):
    user_input = [x for x in jieba.cut(user_input) if x not in stopwords]

    # 因为后面要求交集，所以把用户输入的问题里，在倒排索引中不存在的词先删掉
    for word in user_input:
        if word not in word_docs_dict.keys():
            user_input.remove(word)

    docs_qid = []

    if len(user_input) == 1:
        docs_qid = word_docs_dict[user_input[0]]
    elif len(user_input) > 1:
        # 为了求交集，这里我先取出第一个关键词的文档数组
        first_word = user_input[0]
        docs_qid = word_docs_dict[first_word]

        # 依次取出其余的关键词对应的文档数组，并求交集
        user_input_left = user_input[1:]
        for idx, w in enumerate(user_input_left):
            docs_qid = set(docs_qid).intersection(set(word_docs_dict[w]))

    if len(docs_qid) > 10:
        docs_qid = random.sample(docs_qid, 10)

    # print(docs_qid)
    return user_input, docs_qid


if __name__ == "__main__":
    inverted_index_match()
