import math
import match
import jieba
import pandas as pd


class BM25(object):
    def __init__(self, questions):
        self.D = len(questions)
        self.avgdl = sum(
            [len(question)+0.0 for question in questions]) / self.D
        self.questions = questions
        self.f = []   # 列表的每一个元素是一个dict，dict存储着一个文档中每个词的出现次数
        self.df = {}  # 存储每个词及出现了该词的文档数量
        self.idf = {}  # 存储每个词的idf值
        self.k1 = 1.5
        self.b = 0.75
        self.init()

    def init(self):
        for question in self.questions:
            tmp = {}
            for word in question:
                tmp[word] = tmp.get(word, 0) + 1  # 存储每个文档中每个词的出现次数
            self.f.append(tmp)
            for k in tmp.keys():
                self.df[k] = self.df.get(k, 0) + 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D-v+0.5) - math.log(v+0.5)

    def sim(self, user_input, index):
        score = 0
        for word in user_input:
            if word not in self.f[index]:
                continue
            d = len(self.questions[index])
            score += (self.idf[word]*self.f[index][word]*(self.k1+1)
                      / (self.f[index][word]+self.k1*(1-self.b+self.b*d
                                                      / self.avgdl)))
        return score

    def simall(self, user_input):
        scores = []
        for index in range(self.D):
            score = self.sim(user_input, index)
            scores.append(score)
        return scores


if __name__ == "__main__":
    user_input, docs_qid = match.inverted_index_match()
    # print(user_input)
    with open('data/stopwords.txt') as file:
        stopwords = file.read().split('\n')
    questions = []
    data = pd.read_csv('data/dataset.csv')
    for qid in docs_qid:
        question = data.loc[data.qid == qid, 'question'].values[0]
        question = list(x for x in jieba.cut(question) if x not in stopwords)
        questions.append(question)
    print(questions)
    s = BM25(questions)
    print(f"s.f: {s.f}")
    print(f"s.df: {s.df}")
    print(f"s.idf: {s.idf}")
    rank = s.simall(user_input)
    print(rank)
