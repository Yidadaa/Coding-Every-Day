"""
链表的操作
"""
class ListNode(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

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

def constructList(array):
    """
    从数组构造链表
    Args:
        array: 包含链表元素的数组

    Return:
        List: 链表
    """
    lastNode = None
    for i in range(len(array) - 1, -1, -1):
        tmpNode = ListNode(array[i], lastNode)
        lastNode = tmpNode
    return lastNode