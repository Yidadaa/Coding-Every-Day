"""
二叉树的构造
"""

import math

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None

"""
构造函数
@param: vals: 二叉树的层次遍历节点
@return: root: 二叉树根节点
"""
def constructTree(vals):
    nodes = [TreeNode(val) if val != '#' else None for val in vals]
    count = len(vals)
    for i in range(len(nodes)):
        node = nodes[i]
        i += 1
        if node is not None:
            node.left = None if 2 * i > count else nodes[2 * i - 1]
            node.right = None if 2 * i + 1 > count else nodes[2 * i]
    return nodes[0] if len(nodes) > 0 else None

if __name__ == '__main__':
    vals = [2, 1, 4, '#', 3]
    root = constructTree(vals)
    print(vals)