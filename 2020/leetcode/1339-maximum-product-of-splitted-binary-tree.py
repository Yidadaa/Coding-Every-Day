# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def maxProduct(self, root: TreeNode) -> int:
        self.mod = int(1e9 + 7)
        self.res = 0
        self.count = {}
        self.fab(root)
        self.res_fab(root, 0)
    
        return self.res % self.mod
    
    def fab(self, node):
        if node is None:
            return 0

        left_sum = self.fab(node.left)
        right_sum = self.fab(node.right)
        self.count[node] = (left_sum, right_sum)
        
        return left_sum + right_sum + node.val
        
    def res_fab(self, node, parent):
        if node is None:
            return 0
        
        parent += node.val
        l, r = self.count[node]
        self.res = max((parent + l) * r, (parent + r) * l, self.res)
        self.res_fab(node.left, parent + r)
        self.res_fab(node.right, parent + l)