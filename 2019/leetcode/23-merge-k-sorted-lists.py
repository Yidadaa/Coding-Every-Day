# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        while len(lists) > 1:
            a = lists.pop() if len(lists) > 0 else None
            b = lists.pop() if len(lists) > 0 else None
            lists.insert(0, self.mergeTwoLists(a, b)) # 用append会超时

        return None if len(lists) < 1 else lists[0]
        
    def mergeTwoLists(self, a, b):
        head = ListNode(None)
        node = head
        
        while a is not None and b is not None:
            if a.val <= b.val:
                node.next = a
                a = a.next
            else:
                node.next = b
                b = b.next
            node = node.next
            
        node.next = a if b is None else b

        return head.next
