"""
Definition for singly-linked list.

"""
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    """
    @param: head: a ListNode
    @param: v1: An integer
    @param: v2: An integer
    @return: a new head of singly-linked list
    """
    def swapNodes(self, head, v1, v2):
        """
        问题很简单，但是逻辑比较乱，因为这个是单向链表
        要将某节点的前向节点也保存下来
        """
        iterNode = head
        n1_prev = None
        n1 = None
        n2_prev = None
        n2 = None

        lastNode = None
        headChanged = False
        # 用于标记链表头部是否更换，如果更换，将重新是head指向头部
        while iterNode:
            if iterNode.val == v1:
                n1 = iterNode
                n1_prev = lastNode
                headChanged = headChanged or lastNode is None
                # 如果前向节点是空的，那么就证明头结点变了
            elif iterNode.val == v2:
                n2 = iterNode
                n2_prev = lastNode
                headChanged = headChanged or lastNode is None
            lastNode = iterNode
            iterNode = iterNode.next
        if n1 is None or n2 is None:
            return head
        else:
            if n1_prev:
                n1_prev.next = n2
            if n2_prev:
                n2_prev.next = n1
            if headChanged:
                # 重新指向新的头结点
                head = n2 if n1_prev is None else n1
            swapNext = n1.next
            n1.next = n2.next
            n2.next = swapNext
        return head


def test():
    """
    Test my code
    """
    testValue = [2, 1, 3, 5, 7, 9]
    v1 = 1
    v2 = 9
    lastNode = None
    # 首先按照题目要求初始化一个链表出来
    for i in range(len(testValue) - 1, -1, -1):
        thisNode = ListNode(testValue[i])
        thisNode.next = lastNode
        lastNode = thisNode

    testCase = Solution()
    testRes = testCase.swapNodes(lastNode, v1, v2)
    while testRes is not None:
        print(testRes.val)
        testRes = testRes.next

if __name__ == '__main__':
    test()