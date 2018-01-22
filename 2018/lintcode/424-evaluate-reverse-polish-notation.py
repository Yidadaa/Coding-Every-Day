"""
逆波兰表达式求值

Python与C的整除逻辑不一样：
Python: 
    4 // 5 = 0
    -4 // 5 = -1
C:
    4 / 5 = 0
    -4 / 5 = 0
所以应该这样：
    Python(int(float(-4) / float(5))) == C(-4 / 5)

很傻逼，对吧？
"""

class Solution:
    """
    @param: tokens: The Reverse Polish Notation
    @return: the value
    """
    def evalRPN(self, tokens):
        # write your code here
        num = []
        ops = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: int(float(a) / float(b))
        }
        for t in tokens:
            if t in ops.keys():
                b = num.pop()
                a = num.pop()
                num.append(ops[t](a, b))
            else:
                num.append(int(t))
        return num.pop()

if __name__ == '__main__':
    testClass = Solution()
    testCase = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
    res = testClass.evalRPN(testCase)
    print(res)