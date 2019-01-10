"""
Definition of ListNode
class ListNode(object):

    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""

"""
使用两根指针进行遍历，一根遍历得快，一根遍历得慢，如果两根指针中间相遇了，证明有环；如果有一根指针遇到了结尾，就证明无环。
"""

class Solution:
    """
    @param: head: The first node of linked list.
    @return: True if it has a cycle, or false
    """
    def hasCycle(self, head):
        slow = head
        fast = head
        i = 0
        while i == 0 or slow != fast:
            i += 1
            if fast == None or slow == None:
                return False
            if i % 2 == 0:
                slow = slow.next
            fast = fast.next
        return True