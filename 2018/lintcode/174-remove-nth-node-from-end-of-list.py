"""
删除倒数第n个节点
"""

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
    @return: The head of linked list.
    """
    def removeNthFromEnd(self, head, n):
        node = head
        count = 0
        while node is not None:
            count += 1
            node = node.next
        node = head
        if count == n:
            head = head.next
        else:
            for i in range(0, count - n - 1):
                node = node.next
            if node:
                node.next = node.next.next
        return head