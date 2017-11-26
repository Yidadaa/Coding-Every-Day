'''
对朴素贝叶斯分类器进行评估
'''
import re
import math
import numpy as np
from sklearn.naive_bayes import BernoulliNB
from naiveBayesian import naiveBayesianTextClassifier

def use_sklearn():
    '''
    使用sklearn中的伯努利朴素贝叶斯模型进行计算
    '''
    with open('/home/yida/Desktop/CodingEveryDay/2017/naiveBayesian/input_data.txt') as f:
        file_content = f.readlines()
    input_arr = file_content
    input_arr = [line.split(',') for line in input_arr]
    input_arr = [[int(x) for x in line] for line in input_arr]
    X = [line[1:] for line in input_arr]
    Y = [line[0] for line in input_arr]
    train_data_x = X[0:5000]
    train_data_y = Y[0:5000]
    test_data = X[5000:]
    test_truth = Y[5000:]
    classifier = BernoulliNB()
    classifier.fit(train_data_x, train_data_y)
    test_predict = classifier.predict(test_data)
    right_count = sum([test_predict[i] == test_truth[i] for i in range(len(test_data))])
    print('使用sklearn模型预测：', right_count / len(test_data)) 

def pre_process(row_array):
    '''
    数据预处理，将标注好的数据提取特征并转换为特征向量
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
        print('%0.2f'%(count / len(words)))
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
    # 计算互信息比较费时间，就将特征保存下来
    with open('mi.txt', 'w') as f:
        f.writelines(list(map(lambda x: str(','.join(x) + '\n'), words_MI[0:500])))
        print('done')

    feature_words = [x[0] for x in words_MI[0:500]] # 取500个作为特征词
    feature_array = []
    for line in lower_array:
        line_words = line[1:]
        class_ = 1 if line[0] == 'spam' else 0
        feature = [1 if word in line_words else 0 for word in feature_words]
        feature_array.append([class_] + feature)

    with open('input_data.txt', 'w') as f:
        f.writelines([','.join([str(x) for x in line]) + '\n' for line in feature_array])


if __name__ == '__main__':
    '''
    读取训练数据，训练数据来源：http://www.dt.fee.unicamp.br/~tiago/smsspamcollection/
    '''
    file_content = []
    with open('/home/yida/Desktop/CodingEveryDay/2017/naiveBayesian/trainData/data.txt') as f:
        file_content = f.readlines()

    group_content = {
        'spam': [],
        'ham': []
    }

    # pre_process(file_content)
    use_sklearn()

    sample_count = int(len(file_content) * 0.9) # 取80%做训练集，剩下的做测试集
    for line in file_content[0:sample_count]:
        line_content = line.split('\t')
        if line_content[0] in group_content.keys():
            group_content[line_content[0]].append(line_content[1])

    test_data = file_content[sample_count:]

    print('总数据集大小：', len(file_content))
    print('训练数据集大小：', int(len(file_content) * 0.8))
    print('测试数据集大小：', int(len(file_content) * 0.2))

    my_classifier = naiveBayesianTextClassifier(group_content)
    total = len(test_data)
    right = 0
    for text in test_data:
        text_info = text.split('\t')
        res = my_classifier.predict(text_info[1])
        the_class = 'spam' if res['spam'] > res['ham'] else 'ham'
        if the_class == text_info[0]:
            right += 1
    print('交叉验证结果:', right, '/', total, '=',right / total)
    strings = open('./oral8000.txt').readlines()
    strings = map(lambda x: re.sub(r'[\u4e00-\u9fa5\u3000\n]', '', x), strings)
    strings = list(strings)
    total = len(strings)
    right = 0
    for text in strings:
        res = my_classifier.predict(text)
        the_class = 'spam' if res['spam'] > res['ham'] else 'ham'
        if the_class == 'ham':
            right += 1
    print('口语8000句验证结果:', right, '/', total, '=',right / total)