'''
朴素贝叶斯文本分类器(贝努力模型)
'''
import re
import numpy as np

class naiveBayesianTextClassifier():
    def __init__(self, train_data):
        self.spam_words = self.count(train_data['spam']) # 分别统计垃圾短信和正常短信中的词频
        self.ham_words = self.count(train_data['ham'])
        self.common_words = self.count(train_data['spam'] + train_data['ham'])
        spam_count = len(train_data['spam'])
        ham_count = len(train_data['ham'])
        self.spam_prop = spam_count / (spam_count + ham_count) # 计算垃圾短信的概率
        self.ham_prop = ham_count / (spam_count + ham_count) # 计算正常短信的概率
        self.train_data = train_data
        self.total_count = spam_count + ham_count

    def count(self, array_of_text):
        '''
        统计单词词频，建立字典
        '''
        text_dict = {}
        total_count = len(array_of_text)
        for text in array_of_text:
            words = text.split(' ') # 进行分词
            words = map(lambda x: re.sub(r'\W', '', x).lower(), words) # 对每一个单词全部取小写，并且祛除其中的标点
            words = set(words) # 单词去重
            for word in words: # 统计每个单词出现的次数
                if len(word) == 0:
                    continue
                if word in text_dict.keys():
                    text_dict[word] += 1
                else:
                    text_dict[word] = 2 # 这里进行拉普拉斯平滑
        for word in text_dict:
            text_dict[word] /= total_count + 2 # 计算频率，同样对分母做平滑处理
        return text_dict

    def predict(self, text):
        '''
        进行文本分类
        '''
        words = text.split(' ') # 进行分词
        words = map(lambda x: re.sub(r'\W', '', x).lower(), words) # 对每一个单词全部取小写，并且祛除其中的标点
        words = set(words) # 单词去重
        a = self.spam_prop
        b = self.ham_prop
        for word in words:
            if word in self.common_words:
                # self.common_words[word]
                a *= self.spam_words[word] if word in self.spam_words else 1 / (self.total_count + 2)
                b *= self.ham_words[word] if word in self.ham_words else 1 / (self.total_count + 2)
        
        is_spam = a / (a + b) # 为了便于判断，对a和b进行一些处理
        is_ham = b / (a + b)

        return { 'spam': is_spam, 'ham': is_ham }

class NBClassifier():
    def __init__(self):
        self.groups_prob = {}
        self.class_prior_prob = {}
        self.dimension = 0

    def fit(self, X, Y):
        '''
        训练函数
        '''
        if len(X) != len(Y):
            raise Exception('输入数据维度不相等，请检查数据输入')
        classes = {}
        total_count = len(Y)
        # 先统计所有类别，这里使用拉普拉斯平滑
        for num in Y:
            if num in classes:
                classes[num] += 1
            else:
                classes[num] = 2
        class_prior_prob = {} # 类别的先验概率
        for c in classes:
            class_prior_prob[c] = classes[c] / total_count
        # 然后计算每个类别下，每个特征的概率
        groups = {}
        for i in range(total_count):
            if Y[i] in groups:
                groups[Y[i]].append(X[i])
            else:
                groups[Y[i]] = [X[i]]
        groups_prob = {}
        for g in groups:
            group_data = groups[g]
            feature_count = np.array(group_data).sum(axis=0) # 由于是贝努力模型，每个特征只有0/1两种情况
            groups_prob[g] = (feature_count + 1) / (len(group_data) + 2) # 计算特征存在的概率，应用拉普拉斯平滑
        
        self.groups_prob = groups_prob
        self.class_prior_prob = class_prior_prob
        self.dimension = len(X[0])

    def predict(self, X):
        '''
        预测函数
        '''
        if len(X) == 0:
            return []
        elif len(X[0]) != self.dimension:
            raise Exception('请检查输入数据的维度', self.dimension)
        return_y = []
        for x_val in X:
            p_groups_prob = []
            # 计算每一类的后验概率
            for g in self.groups_prob:
                feature_prob = self.groups_prob[g]
                prob = self.class_prior_prob[g]
                for i in range(len(feature_prob)):
                    if x_val[i] == 1:
                        prob *= feature_prob[i]
                p_groups_prob.append([g, prob])
            # 找出最大后验概率
            p_groups_prob = sorted(p_groups_prob, key=lambda x: x[1], reverse=True)
            return_y.append(p_groups_prob[0][0]) # 返回对应的类别
        return return_y