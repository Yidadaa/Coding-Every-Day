# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        last = None
        h = t = head
        while h is not None:
            should_break = False
            for i in range(k - 1):
                if t.next is None:
                    should_break = True
                    break
                t = t.next
                
            if not should_break:
                t_next = t.next
                t.next = None
                rh, rt = self.reverse(h)
                if last is None:
                    head = rh
                else:
                    last.next = rh
                last = rt
                h = t = t_next
            else:
                if last: last.next = h
                break
        return head
        
    def reverse(self, head):
        h = t = head
        while t and t.next:
            t_next = t.next
            t.next = t_next.next
            t_next.next = h
            h = t_next
        return h, t
        
# 每次只取 k 个节点翻转
