import jieba
import pickle
import random


def inverted_index_match():
    print("请输入你的问题：")

    user_input = input()

    with open('data/stopwords.txt') as file:
        stopwords = file.read().split('\n')

    with open('data/inverted_index.pickle', 'rb') as handle:
        word_docs_dict = pickle.load(handle)

    user_input = [x for x in jieba.cut(user_input) if x not in stopwords]

    print("first_user_input: {user_input}")

    for word in user_input:
        if word not in word_docs_dict.keys():
            user_input.remove(word)

    print("second_user_input: {user_input}")

    docs = []

    if len(user_input) == 1:
        docs = word_docs_dict[user_input[0]]
    elif len(user_input) > 1:
        # 为了求交集，这里我先取出第一个关键词的文档数组
        first_word = user_input[0]
        docs = word_docs_dict[first_word]

        # 依次取出其余的关键词对应的文档数组，并求交集
        user_input = user_input[1:]
        print(user_input)
        for idx, w in enumerate(user_input):
            docs = set(docs).intersection(set(word_docs_dict[w]))

    if len(docs) > 10:
        docs = random.sample(docs, 10)

    print(docs)
    return docs


if __name__ == "__main__":
    inverted_index_match()
