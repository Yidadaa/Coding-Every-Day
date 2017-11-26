'''
朴素贝叶斯文本分类
'''
import json
import math
import numpy as np
import re
def extract_feature(row_array):
    '''
    从原始数据中提取特征词，生成features.json文件
    '''
    words = set()
    words_MI = [] # 保存每个单词的互信息(Mutual Information)
    lower_array = []
    for line in row_array: # 统计所有出现的单词
        [class_, line_text] = line.split('\t')
        line_words = list(map(lambda x: re.sub(r'\W', '', x).lower(), line_text.split(' '))) # 对每一个单词全部取小写，并且祛除其中的标点
        [words.add(x) for x in line_words]
        lower_array.append([class_] + list(line_words)) # 类别， 分词后的短信

    total_count = len(lower_array) + 2
    count = 0
    for word in words: # 对于词表中的每一个单词，计算每个词与分类类别的互信息
        count += 1
        print('%0.2f'%(count / len(words) * 100), '%', end='\r')
        i_x = np.array([1, 1]) # 0：存在，1：不存在
        i_y = np.array([1, 1]) # 0：ham，1：spam
        i_x_y = np.array([[1, 1], [1, 1]]) # 全部赋值为1，做拉普拉斯平滑
        for line in lower_array:
            # 计算word和line的存在情况
            word_is_in_line = 1 if word in line else 0
            class_is_spam = 1 if line[0] == 'spam' else 0
            i_x[word_is_in_line] += 1
            i_y[class_is_spam] += 1
            i_x_y[word_is_in_line][class_is_spam] += 1
        p_x = i_x / total_count
        p_y = i_y / total_count
        p_x_y = i_x_y / total_count
        # 计算互信息
        MI = np.array([[p_x_y[x][y] * math.log2(p_x_y[x][y] / p_x[x] / p_y[y]) for y in [0, 1]] for x in [0, 1]]).sum()
        words_MI.append([word, str(MI)])
    words_MI = sorted(words_MI, key=lambda x: x[1], reverse=True) # 根据互信息进行排序
    with open('./data/features.json', 'w') as f:
        f.write(json.dumps({ 'lower_array': lower_array, 'MI': words_MI }))
