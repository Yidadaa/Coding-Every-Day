"""
反转二叉树
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
    @param: root: a TreeNode, the root of the binary tree
    @return: nothing
    """
    def invertBinaryTree(self, root):
        # write your code here
        stack = [root]
        while len(stack) > 0:
            node = stack.pop()
            if node is None:
                continue
            tmp = node.left
            node.left = node.right
            node.right = tmp
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)
        return root

if __name__ == '__main__':
    from mylib.BiTree import constructTree
    testClass = Solution()
    testCase = constructTree([1, 2, 3, '#', '#', 4])
    res = testClass.invertBinaryTree(testCase)
    print(res)