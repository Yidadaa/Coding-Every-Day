"""
Definition for singly-linked list with a random pointer.
class RandomListNode:
    def __init__(self, x):
        self.label = x
        self.next = None
        self.random = None
"""

"""
这道题有点东西，先用next指针维持链表的前后级关系，然后将random指针复制过去，步骤如下：
1. 原始链表 1[2] -> 2[1] -> 3[1] -> null
2. 第一次复制 1[2] -> (1[*]) -> 2[1] -> (2[*]) -> 3[1] -> (3[*]) -> null
3. 第二次复制 1[2] -> (1[2]) -> 2[1] -> (2[1]) -> 3[1] -> (3[1]) -> null
4. 然后跳格输出即可
"""


class Solution:
    # @param head: A RandomListNode
    # @return: A RandomListNode
    def copyRandomList(self, head):
        node = head
        if head == None:
            return None
        while node != None:
            cloneNode = RandomListNode(node.label)
            cloneNode.next = node.next
            node.next = cloneNode
            node = cloneNode.next
        node = head
        while node != None:
            node.next.random = node.random
            node = node.next.next
        node = head.next
        while node != None and node.next != None:
            node.next = node.next.next
            node = node.next
        return head.next

if __name__ == '__main__':
    from mylib.List import *
    a = constructList([1, 2, 3, 4], RandomListNode)
    b = Solution().copyRandomList(a)
    print(b)