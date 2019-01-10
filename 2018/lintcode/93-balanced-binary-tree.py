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
    @return: True if this Binary tree is Balanced, or false.
    """
    def isBalanced(self, root, depth=0):
        if root == None:
            return depth
        leftDepth = self.isBalanced(root.left, depth + 1)
        rightDepth = self.isBalanced(root.right, depth + 1)
        if leftDepth == False or rightDepth == False:
            return False
        if abs(leftDepth - rightDepth) > 1:
            return False
        else:
            return max([leftDepth, rightDepth]) if depth > 0 else True

if __name__ == '__main__':
    from mylib.BiTree import *
    tree = constructTree([1, 2, 3, '#', '#', 4, 5, '#', '#', '#', '#', 5])
    print(Solution().isBalanced(tree))