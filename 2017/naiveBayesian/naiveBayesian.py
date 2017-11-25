'''
朴素贝叶斯文本分类器
'''
import re

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
                    text_dict[word] = 1
        for word in text_dict:
            text_dict[word] /= total_count # 计算频率
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
                a *= self.spam_words[word] if word in self.spam_words else 1 / self.total_count
                b *= self.ham_words[word] if word in self.ham_words else 1 / self.total_count
        
        is_spam = a / (a + b)
        is_ham = b / (a + b)

        return { 'spam': is_spam, 'ham': is_ham }


if __name__ == '__main__':
    '''
    读取训练数据，训练数据来源：http://www.dt.fee.unicamp.br/~tiago/smsspamcollection/
    '''
    file_content = []
    with open('./trainData/data.txt') as f:
        file_content = f.readlines()

    group_content = {
        'spam': [],
        'ham': []
    }

    sample_count = int(len(file_content) * 0.8) # 取80%做训练集，剩下的做测试集
    for line in file_content[0:sample_count]:
        line_content = line.split('\t')
        if line_content[0] in group_content.keys():
            group_content[line_content[0]].append(line_content[1])

    test_data = file_content[sample_count:]

    test = naiveBayesianTextClassifier(group_content)
    total = len(test_data)
    right = 0
    for text in test_data:
        text_info = text.split('\t')
        res = test.predict(text_info[1])
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
        res = test.predict(text)
        the_class = 'spam' if res['spam'] > res['ham'] else 'ham'
        if the_class == 'ham':
            right += 1
    print('口语8000句验证结果:', right, '/', total, '=',right / total)