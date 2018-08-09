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
    @return: The node where the cycle begins. if there is no cycle, return null
    """
    def detectCycle(self, head):
        slow = head
        fast = head
        meet = None
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                meet = fast
                break
        if not fast or not fast.next:
            return None
        slow = head
        while slow != meet:
            slow = slow.next
            meet = meet.next
        return slow

if __name__ == '__main__':
    from mylib.List import *
    a = constructList([1, 3, 5, 6], cycleIndex=2)
    print(Solution().detectCycle(a))