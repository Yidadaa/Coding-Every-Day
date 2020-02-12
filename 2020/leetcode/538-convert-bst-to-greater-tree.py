# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def convertBST(self, root: TreeNode) -> TreeNode:
        self.s = 0
        self.fab(root)
        return root

    def fab(self, node):
        if node is None: return
        self.fab(node.right)
        self.s += node.val
        node.val = self.s
        self.fab(node.left)

'''
考察二叉树的遍历，刚开始整懵了，递归实现是最简洁的版本。
'''