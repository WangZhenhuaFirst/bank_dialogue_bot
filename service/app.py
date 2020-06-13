import sys
sys.path.append('/Users/huazai/Desktop/学习/项目4/project_4/model')

import match_inverted_index
import match_sentvec
import crawler
from rank import BM25
import pandas as pd


def get_answer():
    print("请输入你的问题：")
    user_input = input()
    user_input_cut, index_docs_qid = match_inverted_index.inverted_index_match(user_input)
    index_docs_questions = []
    data = pd.read_csv('data/dataset.csv')
    for qid in index_docs_qid:
        question = data.loc[data.qid == qid, 'question'].values[0]
        index_docs_questions.append(question)

    sentvec_docs_questions = match_sentvec.sentvec_match(user_input)
    docs_questions = index_docs_questions + sentvec_docs_questions
    sorted_question_scores = BM25.rank(user_input_cut, docs_questions)    
    
    answer = '对不起，我没有听懂您的问题，请把问题描述地详细一点，我会努力理解您的问题的'
    if sorted_question_scores:
        answer = data.loc[data.question == sorted_question_scores[0][0], 'answer'].values[0]
    else:
        question_answer_dicts = crawler.crawl_answer()
        if question_answer_dicts:
            answer = question_answer_dicts[0][1]
    print(answer)
    


if __name__ == '__main__':
    get_answer()