'''
朴素贝叶斯分类器 - 交互式控制台
'''

import json
import numpy as np
import re
from naiveBayesian import NBClassifier
from processData import get_feature_array

print('正在加载模型...')
with open('./data/features.json') as f:
    json_content = f.read()
model = json.loads(json_content)
print('Done.')

print('正在训练...')
lower_array = model['lower_array']
feature_words = [x[0] for x in model['MI']]

train_rate = 1.0 # 把所有数据拿来训练
feature_rate = 0.15
laplace_lambda = 1

total_count = len(lower_array)
train_count = int(total_count * train_rate)
feature_total_count = len(feature_words)
feature_count = int(feature_total_count * feature_rate)

feature_words = feature_words[0:feature_count]

feature_array = get_feature_array(lower_array, feature_words)

X = [line[1:] for line in feature_array]
Y = [line[0] for line in feature_array]

train_data_x = X[0:train_count]
train_data_y = Y[0:train_count]

my_classifier = NBClassifier(laplace_lambda)
my_classifier.fit(train_data_x, train_data_y)

print('Done.')

if __name__ == '__main__':
    while True:
        text = input('请输入要分类的英文句子[Enter输入，CTRL-C退出程序]：\n')
        line_words = list(map(lambda x: re.sub(r'\W', '', x).lower(), text.split(' '))) # 对每一个单词全部取小写，并且祛除其中的标点
        input_array = [1 if word in line_words else 0 for word in feature_words]
        predict = my_classifier.predict([input_array])
        print('<骚扰短信>' if predict[0] == 1 else '<正常短信>', end='\n\n')
