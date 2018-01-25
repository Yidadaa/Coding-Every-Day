"""
二叉树的中序遍历 - 非递归版
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
    @return: Inorder in ArrayList which contains node values.
    """
    def inorderTraversal(self, root):
        # write your code here
        stack = []
        res = []
        p = root
        while len(stack) > 0 or p is not None:
            if p is not None:
                stack.append(p)
                p = p.left
            else:
                p = stack.pop()
                if p is None:
                    break
                res.append(p.val)
                p = p.right
        return res

if __name__ == '__main__':
    from mylib.BiTree import constructTree
    testClass = Solution()
    testCase = []
    res = testClass.inorderTraversal(constructTree(testCase))
    print(res)