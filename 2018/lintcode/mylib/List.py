"""
链表的操作
"""
class ListNode(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

class RandomListNode:
    def __init__(self, x):
        self.label = x
        self.next = None
        self.random = None

def traverseList(l, func=lambda x: x):
    """
    遍历链表
    Args:
        l: 链表
        func: 遍历函数
    """
    while l != None:
        func(l.val)
        l = l.next

def constructList(array, nodeConstructor=ListNode, cycleIndex=-1):
    """
    从数组构造链表
    Args:
        array: 包含链表元素的数组
        nodeConstructor: 不同的链表的类
        tail: 带环链表的入口索引

    Return:
        List: 链表
    """
    lastNode = None
    tail = None
    for i in range(len(array) - 1, -1, -1):
        tmpNode = nodeConstructor(array[i])
        tmpNode.next = lastNode
        if tail == None:
            tail = tmpNode
        lastNode = tmpNode
        if i == cycleIndex:
            tail.next = tmpNode
    return lastNode