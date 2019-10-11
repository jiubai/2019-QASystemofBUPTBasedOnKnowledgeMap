# -*- coding: utf-8 -*-
# !python3
"""
-------------------------------------------------
   File Name：     query_question
   Description :
   Author :       sheng
   date：          2019/9/4
-------------------------------------------------
   Change Activity:
                   2019/9/4:
-------------------------------------------------
"""
# @Site    :
# @File    : main.py
# @Software: PyCharm

import difflib
import docx
import os
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import redis


def jaccard_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))
    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 求交集
    numerator = np.sum(np.min(vectors, axis=0))
    # 求并集
    denominator = np.sum(np.max(vectors, axis=0))
    # 计算杰卡德系数
    return 1.0 * numerator / denominator


class Query():

    def __init__(self):
        r = redis.Redis(host="127.0.0.1", port=6379, db=0)
        self.questions = [q.decode('utf-8') for q in r.keys('*')]
        self.contents = []
        for question in self.questions:
            content = []
            index = 0
            while index < r.llen(question):
                data = r.lindex(question, r.llen(
                    question)-index-1).decode('utf-8')
                if 'image' in data:
                    index += 2
                elif data == '0':
                    index += 1
                else:
                    index += 1
                    content.append(data)
            self.contents.append(content)
        assert len(self.contents) == len(self.questions)
        r.close()

    def query(self, question):
        questions = self.questions
        contents = self.contents
        scores = []
        for index in range(len(questions)):
            f1 = jaccard_similarity(question, questions[index])
            f2 = 0
            for t in contents[index]:
                f2 += jaccard_similarity(question, t)
            f2 /= len(contents[index])
            scores.append(f1*0.7+f2*0.3)  # 不同概率权重
        if max(scores) < 0.5:
            print(max(scores))
        max_index = scores.index(max(scores))
        return questions[max_index]


if __name__ == '__main__':
    query = Query()
    contents = query.contents
    contents = [",".join(content) for content in contents]
    with open("contents.txt", 'w', encoding='utf-8') as f:
        for content in contents:
            f.write(content+"\n")
