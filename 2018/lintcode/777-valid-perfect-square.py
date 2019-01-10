'''
两种解法，一种解法就是使用二分法查找，另一种解法是利用“所有完全平方数都能写做奇数的和”的性质来解

def isPerfectSquare(self, num):
    i = 1
    while num > 0:
        num -= i
        i += 2
    return num == 0
'''

class Solution:
    """
    @param num: a positive integer
    @return: if num is a perfect square else False
    """
    def isPerfectSquare(self, num):
        i = 0
        step = 0

        if num < 0:
            return False
        if num == 0:
            return True

        while True:
            i += 2**step
            if num < i**2:
                i -= 2**step
                step = 0
            elif num == i**2:
                return True
            elif num > i**2 and num < (i + 1)**2:
                return False
    
    def isPerfectSquare2(self, num):
        i = 1
        while num > 0:
            num -= i
            i += 2
        return num == 0

if __name__ == '__main__':
    s = Solution()
    case = [[-1, False], [0, True], [1, True], [2, False], [65536, True]]
    for c in case:
        print(s.isPerfectSquare2(c[0]))