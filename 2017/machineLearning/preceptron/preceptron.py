'''
A simple preceptron code.
'''

data = {
    'positive': [
        [3, 3], [4, 3]
    ],
    'negative': [
        [1, 1]
    ],
    'rate': 1
}

def mutiply(matrix_1, matrix_2):
    if len(matrix_1) != len(matrix_2):
        raise Exception('Wrong dimension')
    return sum([matrix_1[i] * matrix_2[i] for i in range(len(matrix_1))])

def add(matrix_1, matrix_2):
    if len(matrix_1) != len(matrix_2):
        raise Exception('Wrong dimension')
    return [matrix_1[i] + matrix_2[i] for i in range(len(matrix_1))]

def sign(w, b, y, x):
    return y * (mutiply(w, x) + b)

def main():
    points = []
    for i in data['positive']:
        i.append(1)
        points.append(i)
    for i in data['negative']:
        i.append(-1)
        points.append(i)
    rate = data['rate']
    dimension = len(points[0]) - 1
    iter_index = 0
    iter_max = len(points)
    w = [0 for i in range(dimension)]
    b = 0
    while iter_index < iter_max:
        point = points[iter_index]
        x = point[0:dimension]
        y = point[-1]
        if sign(w, b, y, x) <= 0:
            yx = [y * i for i in x]
            w = add(w, yx)
            b = b + y
            iter_index = 0
            print(w, b)
        else:
            iter_index += 1
    print('finally res: ', w, b)

if __name__ == '__main__':
    main()