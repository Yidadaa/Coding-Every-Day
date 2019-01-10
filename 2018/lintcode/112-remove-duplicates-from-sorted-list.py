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
    @return: head of linked list
    """
    def deleteDuplicates(self, head):
        node = head
        while node != None:
            if node.next != None and node.next.val == node.val:
                lastNode = node
                while node != None and node.val == lastNode.val:
                    node = node.next
                lastNode.next = node
                node = lastNode
            node = node.next
        return head

if __name__ == '__main__':
    from mylib.List import *
    a = constructList([1, 2, 2, 4, 1, 1])
    a = Solution().deleteDuplicates(a)
    traverseList(a, lambda x: print(x))