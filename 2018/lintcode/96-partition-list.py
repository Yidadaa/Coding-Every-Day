"""
Definition of ListNode
class ListNode(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""

class Solution:
    """
    @param head: The first node of linked list
    @param x: An integer
    @return: A ListNode
    """
    def partition(self, head, x):
        # 这题很简单，使用两个链表存储两部分，然后最后连接在一起即可
        lessList = None
        lessListHead = None
        largeList = None
        largeListHead = None
        while head != None:
            if head.val < x:
                if lessList == None:
                    lessList = ListNode(head.val, None)
                    lessListHead = lessList
                else:
                    lessList.next = ListNode(head.val, None)
                    lessList = lessList.next
            else:
                if largeList == None:
                    largeList = ListNode(head.val, None)
                    largeListHead = largeList
                else:
                    largeList.next = ListNode(head.val, None)
                    largeList = largeList.next
            head = head.next
        # 如果小于链表为空，则直接返回大于链表，否则就直接将大于链表的头部插到小于链表尾部
        if lessListHead == None:
            return largeListHead
        else:
            lessList.next = largeListHead
            return lessListHead

if __name__ == '__main__':
    from mylib.List import *
    a = constructList([])
    x = 89
    b = Solution().partition(a, x)
    traverseList(b, lambda x: print(x))
