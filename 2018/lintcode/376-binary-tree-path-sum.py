"""
二叉树的路径和
"""

"""
Definition of TreeNode:
"""
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


class Solution:
    """
    @param: root: the root of binary tree
    @param: target: An integer
    @return: all valid paths
    """
    def binaryTreePathSum(self, root, target):
        
        """
        递归遍历二叉树
        @param: node: 树节点
        @param: lastSum: 前向节点和
        @param: path: 前向路径
        @return: path
        """
        def recurveTree(node, path, lastSum):
          if node is None:
            return []
          nextSum = lastSum + node.val
          newPath = []
          newPath.extend(path)
          newPath.append(node.val)
          paths = []
          if node.left is not None:
            paths.extend(recurveTree(node.left, newPath, nextSum))
          if node.right is not None:
            paths.extend(recurveTree(node.right, newPath, nextSum))
          if node.left is None and node.right is None:
            paths = [newPath] if nextSum == target else []
          return paths

        return recurveTree(root, [], 0)
