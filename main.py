# -*- coding: utf-8 -*-
# !python3
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       sheng
   date：          2019/9/4
-------------------------------------------------
   Change Activity:
                   2019/9/4:
-------------------------------------------------
"""
import json

import redis
from tqdm import tqdm

from FeatureProject.bert.tet_bert_keras_sim import SimTwoQuestion
from utils.redis_db import get_data_from_db_by_name, generate_html_by_data
from utils.redis_db import update_history_question, update_common_question
from utils.redis_db import update_QA_db


class Query():

    def __init__(self):
        update_QA_db()
        r = redis.Redis(host="127.0.0.1", port=6379, db=0)
        # self.questions = [q.decode('utf-8') for q in r.keys('*')]
        self.questions_dict = json.load(open('txt_file/questions_dict.json', 'r', encoding="utf-8"))
        self.questions = list(self.questions_dict.keys())
        self.sim_two_question = SimTwoQuestion(self.questions)
        r.close()

    def query(self, question):
        scores = self.sim_two_question.sim_questions(question)
        print(max(scores))
        max_index = scores.index(max(scores))
        print(self.questions[max_index])
        answer_raw = get_data_from_db_by_name(name=self.questions_dict[self.questions[max_index]])
        answer = generate_html_by_data(answer_raw)
        print(answer)
        update_history_question(question)
        update_common_question(question)
        return answer

    def simple_query(self, question):
        scores = self.sim_two_question.sim_questions(question)
        # print(max(scores))
        max_index = scores.index(max(scores))
        # print(self.questions[max_index])
        return self.questions[max_index]


def test_acc():
    with open("./txt_file/questions_dict.txt", 'r', encoding="utf-8") as f:
        all_questions = json.loads(f.read())
    scores = []
    for key, value in all_questions.items():
        print(key)
        length = len(value)
        temp_acc = 0
        for v in value:
            answer = query.simple_query(v)
            if answer == key:
                temp_acc += 1
            else:
                print(v + "      " + answer)
        scores.append(temp_acc / length)
        print(temp_acc / length)
    print(scores)


if __name__ == '__main__':
    query = Query()
    test_acc()

    while True:
        question = input("请输入问题：")
        query.simple_query(question)
