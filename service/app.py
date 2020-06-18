import sys
sys.path.append('/Users/huazai/Desktop/学习/项目4/project_4/model')

import match_inverted_index
import match_sentvec
import crawler
from rank import BM25
import pandas as pd
import re

from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['DEBUG'] = True
Bootstrap(app)

@app.route("/")
def home():    
    return render_template("home.html") 

@app.route("/get")
def get_bot_response():  
    answer = '对不起，我没有听懂您的问题，但我会努力学习的'
    try:
        user_input = request.args.get('msg')
        sentvec_docs_questions = match_sentvec.sentvec_match(user_input)
        if sentvec_docs_questions:
            user_input_cut, index_docs_qid = match_inverted_index.inverted_index_match(user_input)
            index_docs_questions = []
            data = pd.read_csv('data/dataset.csv')
            for qid in index_docs_qid:
                question = data.loc[data.qid == qid, 'question'].values[0]
                index_docs_questions.append(question)

            docs_questions = index_docs_questions + sentvec_docs_questions
            sorted_question_scores = BM25.rank(user_input_cut, docs_questions)
            print(f"first_question: {sorted_question_scores[0]}")    
            answer = data.loc[data.question == sorted_question_scores[0][0], 'answer'].values[0]
        else:
            crawl_answer = crawler.crawl_answer(user_input)
            if crawl_answer:
                answer = crawl_answer
        print(f"answer: {answer}") 
    finally:   
        return answer

if __name__ == "__main__":    
    app.run()


    

