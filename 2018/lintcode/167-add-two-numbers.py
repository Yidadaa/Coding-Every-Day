"""
Definition of ListNode
class ListNode(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""

class Solution:
    """
    @param l1: the first list
    @param l2: the second list
    @return: the sum list of l1 and l2 
    """
    def addLists(self, l1, l2):
        res = None
        last = 0
        l1Num = 0
        l2Num = 0
        head = None
        while l1 != None or l2 != None or last != 0:
            if l1 == None:
                l1Num = 0
            else:
                l1Num = l1.val
                l1 = l1.next
            if l2 == None:
                l2Num = 0
            else:
                l2Num = l2.val
                l2 = l2.next
            s = l1Num + l2Num + last
            unit = s % 10
            last = int(s / 10)
            if res == None:
                res = ListNode(unit, None)
                head = res
            else:
                res.next = ListNode(unit, None)
                res = res.next
        
        return head

if __name__ == '__main__':
    from mylib.List import *
    a = []
    b = []
    a = constructList(a)
    b = constructList(b)
    s = Solution()
    c = s.addLists(a, b)
    traverseList(c, lambda x: print(x))