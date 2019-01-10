"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""

"""
hint: 使用中序遍历输出的二叉查找树的值，就是递增的
"""

class Solution:
    """
    @param root: param root: The root of the binary search tree
    @param k1: An integer
    @param k2: An integer
    @return: return: Return all keys that k1<=key<=k2 in ascending order
    """
    def searchRange(self, root, k1, k2):
        if root == None:
            return []
        res = []
        self.k1 = k1
        self.k2 = k2
        self.doSearch(root, res)
        return res

    def doSearch(self, node, res):
        if not node:
            return
        if node.left:
            self.doSearch(node.left, res)
        if node.val >= self.k1 and node.val <= self.k2:
            res.append(node.val)
        if node.right:
            self.doSearch(node.right, res)

if __name__ == '__main__':
    from mylib.BiTree import *
    tree = constructTree([1, 0.5, 2, 0.1, 0.7, 1.5])
    print(Solution().searchRange(tree, 1, 2))