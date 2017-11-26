'''
朴素贝叶斯文本分类器(贝努力模型)
'''
import re
import numpy as np

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