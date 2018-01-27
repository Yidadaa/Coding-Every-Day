"""
带最小值的栈

实现方法是，最小值也用一个栈来存储，每次pop的时候，把最小值所在的栈尾元素弹出即可
"""

class MinStack:
    
    def __init__(self):
        self.stack = []
        self.minStack = [] # 存最小值的栈

    """
    @param: number: An integer
    @return: nothing
    """
    def push(self, number):
        if len(self.minStack) == 0:
            self.minStack.append(number)
        else:
            curMinEle = self.minStack[-1]
            nextMin = curMinEle if number > curMinEle else number
            self.minStack.append(nextMin)
        self.stack.append(number)
    """
    @return: An integer
    """
    def pop(self):
        self.minStack.pop()
        return self.stack.pop()

    """
    @return: An integer
    """
    def min(self):
        if len(self.minStack) > 0:
            return self.minStack[-1]

if __name__ == '__main__':
    testClass = Solution()
    testCase = []
    res = testClass
    print(res)