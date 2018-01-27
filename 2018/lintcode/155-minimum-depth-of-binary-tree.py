"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""


class Solution:
    """
    @param: root: The root of binary tree
    @return: An integer
    """
    def minDepth(self, root):
        minDep = [1000000000]
        
        if root is None:
            return 0
        
        def iter(node, last):
            if node.left is not None:
                iter(node.left, last + 1)
            if node.right is not None:
                iter(node.right, last + 1)
            if node.left is None and node.right is None:
                minDep[0] = last if last < minDep[0] else minDep[0]
        
        iter(root, 1)
        return minDep[0]