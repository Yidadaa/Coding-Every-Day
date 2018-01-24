"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""


class Solution:
    """
    @param: root: The root of the binary search tree.
    @param: node: insert this node into the binary search tree
    @return: The root of the new binary search tree.
    """
    def insertNode(self, root, node):
        # write your code here
        curNode = root
        if root is None:
            return node
        while True:
            if node.val < curNode.val:
                if curNode.left is None:
                    curNode.left = node
                    break
                else:
                    curNode = curNode.left
            else:
                if curNode.right is None:
                    curNode.right = node
                    break
                else:
                    curNode = curNode.right
        return root

if __name__ == '__main__':
    from mylib.BiTree import constructTree, TreeNode
    testClass = Solution()
    testCase = constructTree([2, 1, 4, '#', 3])
    res = testClass.insertNode(testCase, TreeNode(6))
    print(res)