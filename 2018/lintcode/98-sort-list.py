"""
Definition of ListNode
class ListNode(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""

# 归并排序版本

class Solution:
    """
    @param head: The head of linked list.
    @return: You should return the head of the sorted linked list, using constant space complexity.
    """
    def sortList(self, head):
        # write your code here
        nodeArray = []
        if head == None:
            return head
        i = 0
        node = head
        nextNode = None
        while node != None:
            nextNode = node.next
            if nextNode and node and node.val > nextNode.val:
                node.val, nextNode.val = nextNode.val, node.val
            nodeArray.append(node)
            node = nextNode.next if nextNode != None else None
            if nextNode:
                nextNode.next = None

        while len(nodeArray) > 1:
            a = nodeArray.pop()
            b = nodeArray.pop()
            start = ListNode(None, None)
            newNode = start
            while a and b:
                if a.val < b.val:
                    start.next = a
                    a = a.next
                else:
                    start.next = b
                    b = b.next
                start = start.next
            if a or b:
                start.next = a if b == None else b
            nodeArray.insert(0, newNode.next)
        return nodeArray[0]

if __name__ == '__main__':
    from mylib.List import *
    cases = constructList([1, 2, 9, 6, 4, 8])
    traverseList(Solution().sortList(cases), print)