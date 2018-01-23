"""
两数之和 - 输入是二叉树

还是遍历二叉树，解题思路上没有新意
但是学会了一种新的二叉树遍历方法，使用一个栈来保存待遍历节点
每次从栈顶弹出一个节点，再将其儿子节点入栈，直到栈空，所有的节点就被遍历了一遍
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
    @param: : the root of tree
    @param: : the target sum
    @return: two numbers from tree which sum is n
    """

    def twoSum(self, root, n):
        # write your code here
        queue = [root]
        s = set()
        while len(queue):
            node = queue.pop(0)
            if node is None:
                continue
            if node.val in s:
                return [node.val, n - node.val]
            s.add(n - node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return None