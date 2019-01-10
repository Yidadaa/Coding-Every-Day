"""
Definition of ListNode
class ListNode(object):

    def __init__(self, val, next=None):
        self.val = val
        self.next = next

Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""

class Solution:
    """
    @param: head: The first node of linked list.
    @return: a tree node
    """
    def sortedListToBST(self, head):
        # write your code here
        listVals = []
        while head != None:
            listVals.append(head.val)
            head = head.next
        return self.toBST(listVals)
        
    def toBST(self, nodes):
        n = len(nodes)
        if n == 0:
            return None
        mid = int((n - 1) / 2)
        node = TreeNode(nodes[mid])
        node.left = self.toBST(nodes[0:mid])
        node.right = self.toBST(nodes[mid + 1:])
        return node

if __name__ == '__main__':
    from mylib.BiTree import *
    from mylib.List import *
    a = constructList([1, 2, 3, 4, 5, 6])
    b = Solution().sortedListToBST(a)
    print(b)