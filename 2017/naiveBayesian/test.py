'''
比较自己写的模型与sklearn中模型的性能
'''

import json
from sklearn.naive_bayes import BernoulliNB
from naiveBayesian import NBClassifier
from processData import extract_feature

def pre_process():
    '''
    预处理数据
    '''
    with open('./trainData/data.txt') as f:
        file_content = f.readlines()
    extract_feature(file_content)

def compare():
    with open('./data/features.json') as f:
        json_content = f.read()
    model = json.loads(json_content)
    lower_array = model['lower_array']
    feature_words = [x[0] for x in model['MI']]

    train_rate = 0.9
    total_count = len(lower_array)
    train_count = int(total_count * train_rate)
    feature_rate = 0.3
    feature_total_count = len(feature_words)
    feature_count = int(feature_total_count * feature_rate)

    feature_array = get_feature_array(lower_array, feature_words[0:feature_count])
    
    X = [line[1:] for line in feature_array]
    Y = [line[0] for line in feature_array]

    train_data_x = X[0:train_count]
    train_data_y = Y[0:train_count]
    test_data = X[train_count:]
    test_truth = Y[train_count:]
    classifier = BernoulliNB()
    classifier.fit(train_data_x, train_data_y)
    test_predict = classifier.predict(test_data)
    right_count = sum([test_predict[i] == test_truth[i] for i in range(len(test_data))])
    print('使用sklearn模型预测：', right_count / len(test_data)) 

    my_classifier = NBClassifier()
    my_classifier.fit(train_data_x, train_data_y)
    my_predict = my_classifier.predict(test_data)
    right_count = sum([my_predict[i] == test_truth[i] for i in range(len(test_data))])
    print('我的模型预测：', right_count / len(test_data)) 


def get_feature_array(lower_array, feature_words):
    '''
    预处理数据
    '''
    feature_array = []
    for line in lower_array:
        line_words = line[1:]
        class_ = 1 if line[0] == 'spam' else 0
        feature = [1 if word in line_words else 0 for word in feature_words]
        feature_array.append([class_] + feature)
    return feature_array

# pre_process()
compare()