import jieba
import pickle


# print("请输入你的问题：")
# user_input = input()

user_input = "网银盾补发"

with open('data/stopwords.txt') as file:
    stopwords = file.read().split('\n')

user_input = [x for x in jieba.cut(user_input) if x not in stopwords]

with open('data/inverted_index.pickle', 'rb') as handle:
    word_docs_dict = pickle.load(handle)

# if len(user_input) == 0:
#     return
if len(user_input) == 1:
    if user_input[0] in word_docs_dict.keys():
        docs = word_docs_dict[user_input[0]]
else:
    for index, word in enumerate(user_input):
        if word in word_docs_dict.keys():
            docs = word_docs_dict[word]
            word_index = index
            break
        else:
            continue

    user_input = user_input[word_index+1:]
    print(user_input)
    for idx, w in enumerate(user_input):
        if w in word_docs_dict.keys():
            docs = set(docs).intersection(set(word_docs_dict[w]))

print(docs)
