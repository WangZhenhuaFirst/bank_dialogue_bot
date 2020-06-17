import math
import match_inverted_index
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
            self.idf[k] = math.log(self.D+0.5) - math.log(v+0.5)

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

    def rank(user_input, docs_questions):
        with open('data/stopwords.txt') as file:
            stopwords = file.read().split('\n')
        data = pd.read_csv('data/dataset.csv')
        
        cut_questions = []
        for question in docs_questions:
            question = list(x for x in jieba.cut(question) if x not in stopwords)
            cut_questions.append(question)

        s = BM25(cut_questions)
        scores = s.simall(user_input)
        question_scores = dict(zip(docs_questions, scores))
        sorted_question_scores = sorted(question_scores.items(), key=lambda item:item[1], reverse = True)
        print(sorted_question_scores)
        return sorted_question_scores
        



if __name__ == "__main__":
    print("请输入你的问题：")
    user_input = input()
    user_input, docs_qid = match_inverted_index.inverted_index_match(user_input)
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
    rank = s.simall(user_input)
    print(rank)
