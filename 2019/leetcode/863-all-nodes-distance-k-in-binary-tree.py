# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def distanceK(self, root, target, K):
        """
        :type root: TreeNode
        :type target: TreeNode
        :type K: int
        :rtype: List[int]
        """
        # DFS建邻接图，使用栈来代替递归
        g = { root: set() }
        stack = [root]
        while len(stack) > 0:
            node = stack.pop()
            for child in [node.left, node.right]:
                if child is None: continue
                g[node] |= {child}
                g[child] = {node}
                stack.append(child)
        # BFS搜索距离为K的节点
        visited, queue, d = set(), [target], 0
        while d < K and len(queue) > 0:
            n = len(queue)
            for i in range(n):
                visited.add(queue[i])
                queue += [node for node in g[queue[i]] if node not in visited]
            queue = queue[n:]
            d += 1
        return [x.val for x in queue]
