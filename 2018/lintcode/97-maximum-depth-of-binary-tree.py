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
    @return: An integer
    """
    def maxDepth(self, root, depth=0):
        if root == None:
            return depth
        return max([self.maxDepth(root.left, depth + 1), self.maxDepth(root.right, depth + 1)])

if __name__ == '__main__':
    from mylib.BiTree import *
    tree = constructTree([1])
    print(Solution().maxDepth(tree))