"""
Definition of ListNode
class ListNode(object):

    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""


class Solution:
    """
    @param: head: The first node of linked list.
    @param: n: An integer
    @return: Nth to last node of a singly linked list. 
    """
    def nthToLast(self, head, n):
        m = 0
        node = head
        while node:
            m += 1
            node = node.next
        node = head
        if m < n:
            return None
        while m > n and node:
            m -= 1
            node = node.next
        return node if node == None else node.val

if __name__ == '__main__':
    from mylib.List import *
    cases = constructList([1, 4, 6, 7, 9, 10])
    print(Solution().nthToLast(cases, 7))