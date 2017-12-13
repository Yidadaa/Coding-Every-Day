'''
比较自己写的模型与sklearn中模型的性能
'''

import json
import numpy as np
from sklearn.naive_bayes import BernoulliNB
from naiveBayesian import NBClassifier
from processData import get_feature_array
import timeit

with open('./data/features.json') as f:
    json_content = f.read()
model = json.loads(json_content)

def compare(train_rate=0.9, feature_rate=0.3, laplace_lambda=1):
    lower_array = model['lower_array']
    feature_words = [x[0] for x in model['MI']]

    total_count = len(lower_array)
    train_count = int(total_count * train_rate)
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
    sk_predict = classifier.predict(test_data)

    my_classifier = NBClassifier(laplace_lambda)
    my_classifier.fit(train_data_x, train_data_y)
    my_predict = my_classifier.predict(test_data)

    TFNP_count_sklearn = np.array([[0, 0], [0, 0]]) # 四个值分别是[TN, FP], [FN, TP]
    TFNP_count_me = np.array([[0, 0], [0, 0]])
    for i in range(len(test_data)):
        TFNP_count_sklearn[test_truth[i]][sk_predict[i]] += 1
        TFNP_count_me[test_truth[i]][my_predict[i]] += 1
    return [TFNP_count_sklearn.reshape([1, 4]).tolist()[0], TFNP_count_me.reshape([1, 4]).tolist()[0]]

def compute_P_R_F1(TFNP):
    '''
    计算精确度，召回率和F1值
    '''
    [TN, FP, FN, TP] = TFNP
    A = (TP + TN) / sum(TFNP) # 正确率
    P = TP / (TP + FP) if TP + FP > 0 else 0 # 精确率
    R = TP / (TP + FN) if TP + FN > 0 else 0# 召回率
    F1 = 2 * TP / (2 * TP + FP + FN) if TP + FP + FN > 0 else 0# F1
    return [A, P, R, F1]

data = []
# for i in range(45):
#     start = timeit.default_timer()
#     train_rate = 0.9
#     feature_rate = 0.05 + i / 100
#     [TFNP_sk, TFNP_me] = compare(train_rate, feature_rate)
#     P_R_F1_sk = compute_P_R_F1(TFNP_sk)
#     P_R_F1_me = compute_P_R_F1(TFNP_me)
#     end = timeit.default_timer()
#     data.append([train_rate, feature_rate, P_R_F1_sk, P_R_F1_me, start - end])
#     print('正在执行第%d / 45次计算'%(i + 1), end='\r')

for i in range(45):
    train_rate = 0.9
    feature_rate = 0.15
    laplace_lambda = i / 10
    [TFNP_sk, TFNP_me] = compare(train_rate, feature_rate, laplace_lambda)
    P_R_F1_sk = compute_P_R_F1(TFNP_sk)
    P_R_F1_me = compute_P_R_F1(TFNP_me)
    data.append([train_rate, laplace_lambda, P_R_F1_sk, P_R_F1_me])
    print('正在执行第%d / 45次计算'%(i + 1), end='\r')

# for i in range(5):
#     train_rate = 0.9 - i / 10
#     feature_rate = 0.1
#     [TFNP_sk, TFNP_me] = compare(train_rate, feature_rate)
#     P_R_F1_sk = compute_P_R_F1(TFNP_sk)
#     P_R_F1_me = compute_P_R_F1(TFNP_me)
#     data.append([train_rate, feature_rate, P_R_F1_sk, P_R_F1_me])

with open('./data/res.json', 'w') as f:
    f.write(json.dumps(data))