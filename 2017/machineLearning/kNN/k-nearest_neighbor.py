import math

data = [
    [2, 3], [5, 4], [9, 6],
    [4, 7], [8, 1], [7, 2]
]

class kdTreeNode:
    def __init__(self, data, parent):
        self.data = data
        self.lchild = None
        self.rchild = None
        self.parent = parent
        self.range = None # 所有子树的节点数据集合

class kdTree:
    def __init__(self, training_data):
        self.training_data = training_data
        self.dimension = len(training_data[0])
        self.tree = self.construct_kd_tree(self.training_data)

    def construct_kd_tree(self, data, key_index=0, last_node=None):
        length = len(data)
        if length == 0:
            return None
        index = int(length / 2)
        key_index %= length
        sorted_data = sorted(data, key=lambda x: x[key_index])
        median_point = sorted_data[index] # 获取中位数
        node = kdTreeNode(median_point, last_node)
        node.range = data
        node.lchild = self.construct_kd_tree(sorted_data[0:index], key_index + 1, node) # 分割左侧
        node.rchild = self.construct_kd_tree(sorted_data[index + 1:], key_index + 1, node) # 分割右侧
        return node

    def search(self, target):
        nn = self.tree # find nearest neighbor
        key_index = 0
        min_neighbor = None
        while nn is not None:
            # 找出与target最接近的叶子节点
            min_neighbor = nn
            nn = nn.lchild if target[key_index] < nn.data[key_index] else nn.rchild
            key_index = (key_index + 1) % self.dimension
        min_distance = self.L2_distance(target, min_neighbor.data)
        result = min_neighbor
        while min_neighbor.parent is not None:
            # 从刚才得到的叶子节点向上遍历，找到最接近的树节点
            min_neighbor = min_neighbor.parent
            L2_distance =self.L2_distance(min_neighbor.data, target)
            if L2_distance < min_distance:
                min_distance = L2_distance
                result = min_neighbor
        return result

    def L2_distance(self, point_1, point_2):
        return math.sqrt(sum([(point_1[i] - point_2[i])**2 for i in range(self.dimension)]))

kd_tree = kdTree(data)
target = [9, 7]
res = kd_tree.search(target)
print(res.data)