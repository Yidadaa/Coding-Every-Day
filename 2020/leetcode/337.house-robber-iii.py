# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def rob(self, root: TreeNode) -> int:
        return max(self.fab(root))

    def fab(self, node):
        if node is None: return 0, 0

        lwi, lwo = self.fab(node.left)
        rwi, rwo = self.fab(node.right)

        return node.val + lwo + rwo, max(lwi, lwo) + max(rwi, rwo)

'''
自顶向下递归和自底向上递归的区别。
'''