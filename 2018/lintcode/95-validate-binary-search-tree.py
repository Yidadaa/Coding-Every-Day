"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""

class Solution:
    """
    @param root: The root of binary tree.
    @return: True if the binary tree is BST, or false
    """
    def isValidBST(self, root, min=float('-inf'), max=float('inf')):
        if root == None:
            return True
        return root.val < max and root.val > min and self.isValidBST(root.left, min, root.val) and self.isValidBST(root.right, root.val, max)

if __name__ == '__main__':
    from mylib.BiTree import *
    tree = constructTree([2, 1, 3, 0.5, 1.2, 2.5, 23.4, '#', '#', 1.1, 1.3])
    tree = constructTree([])
    print(Solution().isValidBST(tree))