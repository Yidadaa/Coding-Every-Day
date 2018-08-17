"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""

class Solution:
    """
    @param root: A Tree
    @return: Level order a list of lists of integer
    """
    def levelOrder(self, root):
        if root == None:
            return []
        stack = [root]
        result = []
        while len(stack) > 0:
            newStack = []
            res = []
            for node in stack:
                if node.left:
                    newStack.append(node.left)
                if node.right:
                    newStack.append(node.right)
                res.append(node.val)
            result.append(res)
            stack = newStack
        return result

if __name__ == '__main__':
    from mylib.BiTree import *
    tree = constructTree([1, '#', 2])
    print(Solution().levelOrder(tree))