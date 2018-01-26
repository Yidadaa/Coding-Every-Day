"""
二叉树的前序遍历 - 非递归版
"""

"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""


class Solution:
    """
    @param: root: A Tree
    @return: Preorder in ArrayList which contains node values.
    """
    def preorderTraversal(self, root):
        # write your code here
        stack = [root]
        res = []
        while len(stack) > 0:
            node = stack.pop()
            if node is not None:
                res.append(node.val)
                stack.append(node.right)
                stack.append(node.left)
        return res