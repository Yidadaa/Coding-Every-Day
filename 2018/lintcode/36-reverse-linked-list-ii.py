"""
翻转链表 II

翻转链表中第m个节点到第n个节点的部分

注意：m，n满足1 ≤ m ≤ n ≤ 链表长度

样例
给出链表1->2->3->4->5->null， m = 2 和n = 4，返回1->4->3->2->5->null

挑战 
在原地一次翻转完成
"""


"""
Definition of ListNode
"""
class ListNode(object):

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class Solution:
    """
    @param: head: ListNode head is the head of the linked list 
    @param: m: An integer
    @param: n: An integer
    @return: The head of the reversed ListNode
    """
    def reverseBetween(self, head, m, n):
        count = 1 # 当前节点序号
        node = head
        prevNode = None # 需要交换部分的前向节点
        swapHead = None # 需要交换部分的头节点
        lastNode = None # 当前节点的前向节点
        while node is not None:
            if count > m and count < n:
                # 对于需要交换的部分，直接讲前后两个节点的位置交换即可
                # 但要注意保留后续节点的信息
                nextNode = node.next
                node.next = lastNode
                lastNode = node
                node = nextNode
            else:
                if count == m:
                    # 保留待交换部分的前向节点以及头结点信息
                    prevNode = lastNode
                    swapHead = node
                elif count == n:
                    #　讲交换后的部分插入到链表的正确位置
                    swapHead.next = node.next
                    node.next = lastNode
                    if prevNode is not None:
                        # 转换部分的前向节点不为空时
                        prevNode.next = node
                    else:
                        # 如果为空，证明该节点是头结点，保留头结点信息
                        head = node
                    break
                lastNode = node
                node = node.next
            count += 1
        
        return head

if __name__ == '__main__':
    testClass = Solution()
    testCase = [1]
    head = None
    for i in range(len(testCase) - 1, -1, -1):
        head = ListNode(testCase[i], head)
    newHead = testClass.reverseBetween(head, 1, 1)
    while newHead is not None:
        print(newHead.val)
        newHead = newHead.next