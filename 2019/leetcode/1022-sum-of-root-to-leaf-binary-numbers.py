# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def sumRootToLeaf(self, root: TreeNode) -> int:
        return self.fac(root, 0)
        
    def fac(self, node, s):
        if node is None:
            return 0
        s *= 2
        s += node.val
        if node.left is None and node.right is None:
            return s
        return self.fac(node.left, s) + self.fac(node.right, s)
