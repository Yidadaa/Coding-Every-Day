"""
# Definition for a Node.
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
"""
class Solution:
    def treeToDoublyList(self, root: 'Node') -> 'Node':
        head, tail = self.it(root)
        if head:
            head.left = tail
            tail.right = head
        return head

    def it(self, node):
        if not node: return None, None
        lhead, ltail = self.it(node.left)
        rhead, rtail = self.it(node.right)
        if ltail:
            ltail.right = node
            node.left = ltail
        else:
            lhead = node
        if rhead:
            rhead.left = node
            node.right = rhead
        else:
            rtail = node
        return lhead, rtail