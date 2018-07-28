"""
Definition of ListNode
class ListNode(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""
"""
很有意思的一道题，覆盖了链表几种基本操作：原地翻转链表、取链表中点
"""

class Solution:
    """
    @param head: The head of linked list.
    @return: nothing
    """
    def reorderList(self, head):
        # write your code here
        if head == None or head.next == None:
            return head
        fast = head
        slow = head
        last = None
        # 使用快慢指针法找出链表中点
        while fast.next != None and fast.next.next != None:
            last = slow
            slow = slow.next
            fast = fast.next.next
        if fast.next != None:
            # 偶数链表
            last = slow
            slow = slow.next
        last.next = None
        mid = slow
        # 翻转后半段链表
        mid = self.reverse(mid)
        h1 = head
        h2 = mid
        last = None
        # 将两节链表交叉拼接起来，完成算法
        while True:
            tmp1 = h1.next
            tmp2 = h2.next
            h1.next = h2
            h2.next = tmp1
            last = h2
            h1 = tmp1
            h2 = tmp2
            if h1 == None:
                last.next = h2
                break
        return head

    """
    @param node: 链表头节点
    @return: 翻转后的链表
    """
    def reverse(self, node):
        if node == None or node.next == None:
            return node
        h = node
        n = node.next
        while n != None:
            tmp = n.next
            n.next = h
            h = n
            n = tmp
        node.next = None
        return h

if __name__ == '__main__':
    from mylib.List import *
    s = Solution()
    a = constructList([1])
    # rb = s.reverse(a)
    c = s.reorderList(a)
    traverseList(c, print)