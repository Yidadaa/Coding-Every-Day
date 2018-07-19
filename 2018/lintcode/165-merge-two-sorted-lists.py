"""
Definition of ListNode
class ListNode(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""

class Solution:
    """
    @param l1: ListNode l1 is the head of the linked list
    @param l2: ListNode l2 is the head of the linked list
    @return: ListNode head of linked list
    """
    def mergeTwoLists(self, l1, l2):
        resList = None
        listHead = None
        while l1 != None or l2 != None:
            if l1 == None:
                l1Val = float('inf')
            else:
                l1Val = l1.val
            if l2 == None:
                l2Val = float('inf')
            else:
                l2Val = l2.val
            if l1Val < l2Val:
                val = l1Val
                l1 = l1.next
            else:
                val = l2Val
                l2 = l2.next
            if resList == None:
                resList = ListNode(val, None)
                listHead = resList
            else:
                resList.next = ListNode(val, None)
                resList = resList.next
        return listHead

if __name__ == '__main__':
    from mylib.List import *
    a = constructList([1, 3, 5, 8])
    b = constructList([])
    c = Solution().mergeTwoLists(a, b)
    traverseList(c, lambda x: print(x))