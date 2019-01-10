"""
Definition of ListNode

class ListNode(object):

    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""

class Solution:
    """
    @param head: n
    @return: The new head of reversed linked list.
    """
    def reverse(self, head):
        # write your code here
        lastNode = None
        while head != None:
            tmpNode = head.next
            head.next = lastNode
            lastNode = head
            head = tmpNode
        return lastNode

if __name__ == '__main__':
    from mylib.List import *
    a = constructList([1, 2, 3, 4])
    b = Solution().reverse(a)
    traverseList(b, lambda x: print(x))
