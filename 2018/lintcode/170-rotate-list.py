"""
Definition of ListNode
class ListNode(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""

class Solution:
    """
    @param head: the List
    @param k: rotate to the right k places
    @return: the list after rotation
    """
    def rotateRight(self, head, k):
        tail = None
        kNode = None
        i = 0
        l = 0
        node = head
        while node != None:
            l += 1
            node = node.next

        if l == 0:
            return head

        k %= l # 对超出k的部分进行截取

        # 不需要移动
        if k == 0:
            return head

        node = head
        while node != None:
            i += 1
            if i == l - k + 1:
                kNode = node
            if i == l:
                tail = node
            elif i == l - k:
                tmpNode = node.next
                node.next = None
                node = tmpNode
            else:
                node = node.next
        if tail != None:
            tail.next = head
        return kNode

if __name__ == '__main__':
    from mylib.List import *
    a = constructList([1, 2, 4])
    b = 4
    c = Solution().rotateRight(a, b)
    traverseList(c, lambda x: print(x))