'''
决策树生成算法
包含ID3和C4.5两种经典算法。
只提供一个ID3的实例，C4.5与ID3只是特征选择函数不同。
'''
import math

training_data = {
    'features': [
        '年龄', '有工作', '有房子', '信贷情况', '类别'
    ],
    'data': [
        ['青年', '否', '否', '一般', '否'],
        ['青年', '否', '否', '好', '否'],
        ['青年', '是', '否', '好', '是'],
        ['青年', '是', '是', '一般', '是'],
        ['青年', '否', '否', '一般', '否'],
        ['中年', '否', '否', '一般', '否'],
        ['中年', '否', '否', '好', '否'],
        ['中年', '是', '是', '好', '是'],
        ['中年', '否', '是', '非常好', '是'],
        ['中年', '否', '是', '非常好', '是'],
        ['老年', '否', '是', '非常好', '是'],
        ['老年', '否', '是', '好', '是'],
        ['老年', '是', '否', '好', '是'],
        ['老年', '是', '否', '非常好', '是'],
        ['老年', '否', '否', '一般', '否'],
    ]
}

class ID3TreeNode:
    def __init__(self, type, instances, parent=None, featurename=None):
        self.type = type # 最终分类
        self.instances = instances # 节点代表的子树所包含的所有实例，实例是训练集中的数据
        self.children = None # ID3TreeNode dict
        self.featurename = featurename # 对应的特征名称
        self.parent = parent # 父节点

class ID3Tree:
    def __init__(self, training_data, full_features, threshold):
        self.training_data = training_data # 训练数据集
        self.threshold = threshold # 阈值
        self.full_features = full_features # 特征集
        self.tree = self.generate_tree(training_data) # 生成决策树
        self.leaf_nodes = self.get_leaf_nodes(self.tree)

    def generate_tree(self, data, parent=None):
        '''
        @param {List} data 训练数据集
        @param {Set} 特征集
        @return {ID3TreeNode} 生成的子树
        '''
        count = len(data) # 数据集观测点数量
        available_features = []
        if count == 0:
            return None
        C_k = self.group_by_index(data, -1) # 数据分组
        dimision = len(data[0])
        classes = list(C_k.keys())
        for i in range(dimision - 1): # 遍历data的每一个特征
            class_num = len(set([k[i] for k in data]))
            if class_num > 1: # 如果某特征下含有多于两个可选值，就将其列为可用特征
                available_features.append(i)
            
        if len(C_k) == 1:
            # 如果数据集中所有实例同属于一类，则返回一个单节点树，节点类为该类
            class_ = classes[0]
            return ID3TreeNode(type=class_, instances=data, parent=parent)
        if len(available_features) == 0:
            # 如果可用特征集为空，就返回一个单节点树，节点的类由所有实例投票产生
            class_ = self.vote_for_main_class(data, -1)
            return ID3TreeNode(type=class_, instances=data, parent=parent)
        else:
            # 计算训练集中各特征的信息增益
            H_D = 0 # 经验熵
            for key in C_k:
                key_rate = len(C_k[key]) / count
                H_D += key_rate * math.log2(key_rate)
            H_D = - H_D # 取负数
            H_D_A = [] # 经验条件熵，第index项数据对应者第index个feature的经验条件熵，用于debug
            H_D_A_max_index = 0 # 使经验条件熵最大的特征索引
            H_D_A_max = 0 # 经验条件熵最大值，用于控制阈值
            H_D_A_max_group = {} # 最大特征A对应的的数据分组
            for index in available_features: # 对于每一个可用特征，计算经验条件熵
                data_A_k_group = self.group_by_index(data, index) # 以特征A(k)分类的数据
                H_D_A_k = 0 # 经验条件熵
                for A_k in data_A_k_group:
                    # 计算按照特征A(k)分组后的子集数据的经验熵
                    A_k = data_A_k_group[A_k]
                    H_D_A_k += self.count_H_D(A_k) * len(A_k) / count # 计算经验条件熵
                H_D_A_k = H_D - H_D_A_k # 计算信息增益
                if H_D_A_k > H_D_A_max:
                    # 记录最大经验条件熵对应的特征
                    H_D_A_max = H_D_A_k
                    H_D_A_max_index = index
                    H_D_A_max_group = data_A_k_group
                H_D_A.append(H_D_A_k)
            # 如果最大信息增益小于阈值，就返回单节点树
            class_ = self.vote_for_main_class(data, -1)
            featurename = self.full_features[H_D_A_max_index]
            ID3_sub_tree = ID3TreeNode(type=class_, instances=data, featurename=featurename, parent=parent)
            if H_D_A_max > self.threshold:
                ID3_chilren = {} # 由最优特征值所有可能取值作为索引
                for group in H_D_A_max_group:
                    # 对最优划分的每一个子集进行迭代生成子树
                    ID3_chilren[group] = self.generate_tree(H_D_A_max_group[group], ID3_sub_tree)
                ID3_sub_tree.children = ID3_chilren
            return ID3_sub_tree

    def count_H_D(self, data):
        '''
        @name 计算经验熵
        @data 数据集
        @return number
        '''
        C_k = self.group_by_index(data, -1) # 按分类结果进行分组
        count = len(data) # 数据集观测点数量
        if count == 0:
            return 0
        dimision = len(data[0])
        H_D = 0 # 经验熵
        for key in C_k:
            key_rate = len(C_k[key]) / count
            H_D += key_rate * math.log2(key_rate)
        return -H_D

    def vote_for_main_class(self, data, index):
        '''
        @name 接收一个M×N的矩阵，返回第index列投票产生的优势值
        @return {String or Number}
        '''
        group = self.group_by_index(data, index)
        classes = list(group.keys())
        class_count = 0
        main_class = classes[0]
        for key in classes:
            # 进行投票
            if len(group[key]) > class_count:
                class_count = len(group[key])
                main_class = key
        return main_class

    def group_by_index(self, data, index):
        '''
        @name 将一个M×N的矩阵按照第index列的值分组
        @return {Object} 分组后的字典，字典的键是原矩阵第index列的取值集合
        '''
        group = {}
        for i in data:
            group_name = i[index]
            if group_name in group:
                group[group_name].append(i)
            else:
                group[group_name] = [i]
        return group

    def get_leaf_nodes(self, node):
        '''
        @name 获取所有的叶节点，每执行一次本函数，就遍历一遍树
        '''
        leaf_nodes = []
        if node.children is not None:
            for childname in node.children:
                child = node.children[childname]
                leaf_nodes.extend(self.get_leaf_nodes(child))
        else:
            leaf_nodes.append(node)
        return leaf_nodes

    def pruning(self):
        '''
        @name 决策树的剪枝
        @desc 剪枝策略：只有某个叶节点的兄弟节点均为叶节点时，才有可能对其进行剪枝操作
        '''
        last_sub_leaves = set([])
        while True:
            self.leaf_nodes = self.get_leaf_nodes(self.tree) # 重新获取叶子节点
            sub_leaves_pre = set([leaf.parent for leaf in self.leaf_nodes]) # 取父节点并去重
            to_be_removed = set([])
            for node in sub_leaves_pre:
                for child in node.children:
                    # 对于某次叶节点，如果其子节点存在非叶节点，则将其标记为待剔除节点
                    child = node.children[child]
                    if child.children is not None:
                        to_be_removed.add(node)
            sub_leaves = sub_leaves_pre - to_be_removed # 剔除不满足条件的节点
            if sub_leaves == last_sub_leaves:
                # 如果节点没有发生变化，证明剪枝已经完成，结束循环
                break
            last_sub_leaves = sub_leaves
            for sub_leaf in sub_leaves:
                # 开始计算损失函数
                cost_before = sum([self.cost_function(sub_leaf.children[i]) for i in sub_leaf.children]) # 计算子节点的加权经验熵
                cost_after = self.cost_function(sub_leaf) # 计算父节点包含实例的经验熵
                if cost_after <= cost_before:
                    # 如果剪枝后的损失函数变小了，那么就执行剪枝操作
                    sub_leaf.children = None

    def cost_function(self, node):
        '''
        @name 决策树修剪时的cost function
        '''
        instances = node.instances
        return self.count_H_D(instances) * len(instances) / len(self.training_data)


test_tree = ID3Tree(training_data=training_data['data'], full_features=training_data['features'], threshold=0.01)
test_tree.pruning()
pass