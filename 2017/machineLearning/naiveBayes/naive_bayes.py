'''
没有做拉普拉斯平滑的朴素贝叶斯分类器
如果要做拉普拉斯平滑，那就在计算条件概率的时候，分子加λ，分母加k*λ
其中k是分类数
'''

data = [
    #x1, x2, y
    [1, 'S', -1],
    [1, 'M', -1],
    [1, 'M', 1],
    [1, 'S', 1],
    [1, 'S', -1],
    [2, 'S', -1],
    [2, 'M', -1],
    [2, 'M', 1],
    [2, 'L', 1],
    [2, 'L', 1],
    [3, 'L', 1],
    [3, 'M', 1],
    [3, 'M', 1],
    [3, 'L', 1],
    [3, 'L', -1]
]

test = [2, 'S']

def conditional_probability(data):
    '''
    @name 计算条件概率
    @param data: 源数据
    @param key_index: 分组依据
    @return{List} result: 条件概率
    '''
    result = []
    dimension = len(data[0])
    N = len(data)
    for key_index in range(dimension - 1):
        # 对输入变量x的每一维所有可能的取值计算其条件概率
        grouped_data = {}
        for i in data:
            if i[key_index] not in grouped_data:
                grouped_data[i[key_index]] = 1
            else:
                grouped_data[i[key_index]] += 1
        for i in grouped_data:
            # 转换为概率
            grouped_data[i] = grouped_data[i] / N
        result.append(grouped_data)
    
    return result

def posterior_probability(y_probability, hash_data, input_data):
    '''
    @name 计算后验概率
    @param{dict} y_probability: 存储每一个class的先验概率，key是类名，value是概率
    @param{dict} hash_data: 存储输入变量的每一维所有可能取值的条件概率，结构
                    hash_data: { <- dict
                        [class_name]: [ <- list
                            [list_index]: { <- dict
                                [第list_index维的x向量所有可能取值]: 对应概率
                            }
                        ]
                    }
    '''
    result = {}
    for i in hash_data:
        con_p = hash_data[i]
        p = y_probability[i]
        for index in range(len(input_data)):
            p *= con_p[index][input_data[index]]
        result[i] = p
    return result

def main():
    hash_data = {}
    x_dimension = len(data[0]) - 1
    y_probability = {}

    for i in data:
        y = i[-1]
        # 按照y进行分组
        if y not in hash_data:
            hash_data[y] = [i]
        else:
            hash_data[y].append(i)

    for i in hash_data:
        # 计算y的先验概率
        y_probability[i] = len(hash_data[i]) / len(data)

    for i in hash_data:
        # 计算条件概率
        hash_data[i] = conditional_probability(hash_data[i])

    p_p = posterior_probability(y_probability, hash_data, test)
    p = 0
    class_name = None
    for i in p_p:
        if p_p[i] > p:
            p = p_p[i]
            class_name = i
        print('y=', i, '的后验概率是：', p_p[i])

    print('输入值', test, '被分类为：', class_name)

main()