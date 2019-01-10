"""
Definition of ListNode
class ListNode(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""

class Solution:
    """
    @param head: head is the head of the linked list
    @return: head of the linked list
    """
    def deleteDuplicates(self, head):
        resHead = None
        node = head
        lastNode = None
        while node:
            if node.next and node.next.val != node.val:
                if resHead == None:
                    resHead = node
                lastNode = node
                node = node.next
            else:
                if not node.next:
                    break
                while node.next and node.next.val == node.val:
                    node = node.next
                if lastNode:
                    lastNode.next = node.next
                elif node.next and node.next.next and node.next.next.val != node.next.val:
                    lastNode = node.next
                    resHead = lastNode
                node = node.next
        return resHead
