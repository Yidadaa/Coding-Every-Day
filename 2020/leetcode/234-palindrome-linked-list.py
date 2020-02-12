# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        node, n = head, 0
        while node:
            node = node.next
            n += 1
        if n <= 1: return True

        node = head
        for i in range(n // 2 - 1):
            node = node.next
        last_half = node.next.next if n % 2 else node.next
        node.next = None
        last_half = self.reverse(last_half)
        while head and last_half:
            if head.val != last_half.val:
                return False
            head = head.next
            last_half = last_half.next
        return True

    def reverse(self, node):
        if node is None: return node
        last, node = node, node.next
        while node:
            _node = node.next
            node.next = last
            last = node
            node = _node
        return last

'''
简单综合题，先翻转后半部分，然后对比。
'''