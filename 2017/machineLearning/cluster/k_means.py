'''
实现k_means算法
'''
import math
import random

def computeDistance(p1, p2):
    # 计算两点之间的距离
    qlen = 0
    for i in range(len(p1)):
        qlen += (p1[i] - p2[i])**2
    return math.sqrt(qlen)

def k_means(k = 5, file_name = 'data'):

    data = None

    with open(file_name) as f:
        data = f.readlines()
        data = map(lambda x: list(map(float, x.split(' '))), data)
        data = list(data)

    x_range = [1000000, -1000000] # 数据点的x范围
    y_range = [1000000, -1000000] # 数据点的y范围

    # 取x和y的最大最小范围
    for point in data:
        x_range[0] = point[0] if point[0] < x_range[0] else x_range[0]
        x_range[1] = point[0] if point[0] > x_range[1] else x_range[1]
        y_range[0] = point[1] if point[1] < y_range[0] else y_range[0]
        y_range[1] = point[1] if point[1] > y_range[1] else y_range[1]

    # 取k个中心点
    k_mean_points = []
    for i in range(k):
        point = [0, 0]
        point[0] = random.uniform(x_range[0], x_range[1])
        point[1] = random.uniform(y_range[0], y_range[1])
        k_mean_points.append(point)

    k_mean_groups = [[] for i in range(k)]



    while True:
        never_move_point = 0 # 记录不再移动的中心点的个数
        for point in data:
            class_ = None
            min_distance = 10000000
            for index in range(k):
                distance = computeDistance(k_mean_points[index], point)
                if distance < min_distance: # 找出距离该点最近的中心点
                    class_ = index
                    min_distance = distance
            k_mean_groups[class_].append(point) # 将该点分到对应的类里面去
        # 重新计算各类的中心点
        for i in range(k):
            if len(k_mean_groups[i]) == 0:
                never_move_point += 1
                continue
            group_x = [p[0] for p in k_mean_groups[i]]
            group_y = [p[1] for p in k_mean_groups[i]]
            new_mean = [sum(group_x) / len(group_x), sum(group_y) / len(group_y)] # 计算当前簇的中心点
            if computeDistance(new_mean, k_mean_points[i]) < 0.01:
                never_move_point += 1
            k_mean_points[i] = new_mean
        if never_move_point == k: # 当所有点不再移动时，停止迭代
            break
    
    return k_mean_groups

# print('debugger')


if __name__ == '__main__':
    k_means()